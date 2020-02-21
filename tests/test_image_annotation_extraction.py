# -*- coding: utf-8 -*-

from .context import eatyourlooks

from tests.helpers import *

import unittest
import os
import io


class DocumentExtractionTestSuite(unittest.TestCase):
    """Test cases."""

    # shared test resources
    #image_file = os.path.abspath('tests/images/caponata-cropped.jpg')
    with io.open("tests/expected_values/expected_document", 'r') as exp_file:
        document = exp_file.read()
        document = str(document)

    def test_get_bounds(self):
        full_api_response = load_api_response_from_file("tests/inputs/parsed-caponata-cropped")
        text_annotation = full_api_response.full_text_annotation



        bounds = eatyourlooks.get_document_block_bounds(text_annotation)
        self.assertIsNotNone(bounds)
        #self.assertEqual(str(document_of_image), self.expected_document)



if __name__ == '__main__':
    unittest.main()
