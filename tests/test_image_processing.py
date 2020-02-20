# -*- coding: utf-8 -*-

from .context import eatyourlooks
from google.cloud import vision

import unittest
import os


class ImageProcessingTestSuite(unittest.TestCase):
    """Test cases."""
    image_file = os.path.abspath('tests/images/caponata-cropped.jpg')

    def test_parse(self):
        client = vision.ImageAnnotatorClient()        
        self.assertFalse(eatyourlooks.parse_image_for_text(client, self.image_file))


if __name__ == '__main__':
    unittest.main()
