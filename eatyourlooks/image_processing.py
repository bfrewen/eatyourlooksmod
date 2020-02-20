import io
from google.cloud import vision
from google.cloud.vision import types

def parse_image_for_text(client, file_path):
    # Call the client to extract the full text annotation from the given image.
    # client (ImageAnnotatorClient): the client object for the API
    # file_path (string): full path to image file
    # returns: AnnotateImageResponse

    # open file
    with io.open(file_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    return False
