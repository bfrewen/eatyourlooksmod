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
