from enum import Enum
import io
import os
import sys

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def main():
    print('hi')

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.abspath('../eatyourlooksmod/images/caponata-cropped.jpg')
    file_name = os.path.abspath('../eatyourlooksmod/images/caponata-full.jpg')
    file_name = os.path.abspath('../eatyourlooksmod/images/luffa-with-beef.jpg')
    print(file_name)

    print('look for fancy text')
    parsed_image = detect_medium_text(client, file_name)

    print('pick your boxes')
    box_idx_per_category = assign_boxes_to_info()
    print(box_idx_per_category)

    print('extract the text')
    text_per_category = extract_text_from_boxes(box_idx_per_category, parsed_image) 

def detect_text(client, file_path):
    print('texty')
    with io.open(file_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    #print(dir(response))
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def get_document_feature_bounds(document, feature_type):
    print("getting features for " + str(feature_type))
    bounds = []

    for i,page in enumerate(document.pages):
        for block in page.blocks:
            if feature_type ==FeatureType.BLOCK:
                bounds.append(block.bounding_box)
            for paragraph in block.paragraphs:
                if feature_type ==FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature_type == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)
                    if (feature_type == FeatureType.WORD):
                        bounds.append(word.bounding_box)
    return bounds

def draw_numbers(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    #for bound in bounds:
    for idx, bound in enumerate(bounds):
        print("index is " + str(idx) + "at " + str(bound.vertices[0].x) + 
              "," + str(bound.vertices[0].y))
        draw.text([bound.vertices[0].x, bound.vertices[0].y], str(idx), fill=color)
    return image

def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, color)
    return image


def detect_medium_text(client, file_path):
    # code written from playing with the medium post on ocr
    print('textish')
    with io.open(file_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    
    # get bounds for some feature type
    bounds = get_document_feature_bounds(document, FeatureType.BLOCK)

    # draw the boxes in the image
    image = Image.open(file_path)
    boxes_image = draw_boxes(image, bounds, 'blue')
    numbers_plus_boxes_image = draw_numbers(image, bounds, 'blue')
    numbers_plus_boxes_image.show()
    
    return document

    # for reference
    # full_text_annotation -> Page -> Block -> Paragraph -> Word -> Symbols
    good_part_of_response = response.full_text_annotation

    print(good_part_of_response)
    return


def assign_boxes_to_info():
    categories = ['title', 'ingredients', 'page number']
    dict_of_categories = {}
    for category in categories:
        value = input("Box number for " + category + "\n")
        print(f'You entered {value}')
        dict_of_categories[category] = int(value)
    return dict_of_categories

def extract_text_from_boxes(box_idx_per_category, parsed_image):
    # given a dict of box ids for each category, return the text in each of those boxes

    # collect the results here
    text_per_category = {}

    for category, box_id in box_idx_per_category.items():
        print(f"getting text for '{category}', id {box_id}")
        if box_id != -1:
            found_text = text_in_box(parsed_image, box_id)
            text_per_category[category] = found_text

    return text_per_category

def text_in_box(parsed_image, box_id):
    breaks = vision.enums.TextAnnotation.DetectedBreak.BreakType               
    # assume one page
    my_block = parsed_image.pages[0].blocks[box_id]
    paragraphs = []
    lines = []
    reconstructed_string = ""
    print("looking now...")
    for paragraph in my_block.paragraphs:
        current_para_as_string = ""
        current_line_as_string = ""
        for word in paragraph.words:
            for symbol in word.symbols:
                reconstructed_string += symbol.text   # old, no formatting
                current_line_as_string += symbol.text # new, with formatting

                if symbol.property.detected_break.type == breaks.SPACE:
                    current_line_as_string += ' '
                if symbol.property.detected_break.type == breaks.EOL_SURE_SPACE:
                    # new line with space at end
                    current_line_as_string += ' '
                    lines.append(current_line_as_string)
                    current_para_as_string += current_line_as_string
                    current_line_as_string = ''
                if symbol.property.detected_break.type == breaks.LINE_BREAK:
                    # new line with no space
                    lines.append(current_line_as_string)
                    current_para_as_string += current_line_as_string
                    current_line_as_string = ''
        # edge case for single line
        if not current_para_as_string:
            current_para_as_string += current_line_as_string

        paragraphs.append(current_para_as_string)

    #print(f"for box {box_id} I constructed '{reconstructed_string}'")
    print(f"with breaks: {paragraphs}")

#def get_bounding_box_as_coord_tuple(bounding_box):
#    coord_tuple = []
#    for vert in bounding_box.vertecies:
#        coord_tuple.append(vert.x, vert.y)
#    return coord_tuple 

def text_within_coords(parsed_image, coord_tuple):
    # for the given coordiantes, return all of the text
    # e.g. should reproduce the text in a given bouding box
    print(f'given coord tuple({coord_tuple[0]}, {coord_tuple[1]}, {coord_tuple[2]}, {coord_tuple[3]})')
    pass

def find_labels(client, file_name):
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    print('Labels:')
    for label in labels:
        print(label.description)

if __name__ == "__main__":
    main()
