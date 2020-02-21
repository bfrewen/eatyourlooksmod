from google.cloud.vision_v1.proto import image_annotator_pb2

import io

def write_api_response_to_file(response, filename):
    """Use this for creating test fixtures"""
    # open file for writing
    # serialize response to string response.SerializeToString()
    # write string to file
    with io.open(filename, 'wb') as out_file:
        out_file.write(response.SerializeToString())


def load_api_response_from_file(filename):
    # create an empty response object 
    rehydrated_from_file = image_annotator_pb2.AnnotateImageResponse()

    # open file for reading  
    with io.open(filename, 'rb') as in_file:
        file_as_string = in_file.read()
        # fill it with the string read from the file
        rehydrated_from_file.ParseFromString(file_as_string)

    return rehydrated_from_file

def create_text_fixture(self):
    # it's temp, I promise
    client = vision.ImageAnnotatorClient()
    with io.open(self.image_file, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    api_response = client.document_text_detection(image=image)

    print("")
    print(type(api_response))
    print(dir(api_response))
    with io.open("tests/inputs/parsed-caponata-cropped", 'wb') as out_file:
        out_file.write(api_response.SerializeToString())
     # pause, take a deep breath and see if our file worked
    doc_from_file = load_api_response_from_file("tests/inputs/parsed-caponata-cropped")
    for page in doc_from_file.full_text_annotation.pages:
        print('hey, a page!!')

