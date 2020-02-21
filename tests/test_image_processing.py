# -*- coding: utf-8 -*-

from .context import eatyourlooks
from google.cloud import vision

from tests.helpers import *

import unittest
import os
import io


class ImageProcessingTestSuite(unittest.TestCase):
    """Test cases."""

    # shared test resources
    image_file = os.path.abspath('tests/images/caponata-cropped.jpg')
    with io.open("tests/expected_values/expected_document", 'r') as exp_file:
        expected_document = exp_file.read()
        expected_document = str(expected_document)

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


    def test_parse_image(self):
        client = vision.ImageAnnotatorClient()        
        document_of_image = eatyourlooks.parse_image_for_text(client, self.image_file)
        self.assertEqual(str(document_of_image), self.expected_document)


if __name__ == '__main__':
    unittest.main()
