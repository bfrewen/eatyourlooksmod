# -*- coding: utf-8 -*-

from .context import eatyourlooks
from google.cloud import vision

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

    def test_parse_image(self):
        client = vision.ImageAnnotatorClient()        
        document_of_image = eatyourlooks.parse_image_for_text(client, self.image_file)
        self.assertEqual(str(document_of_image), self.expected_document)


if __name__ == '__main__':
    unittest.main()
