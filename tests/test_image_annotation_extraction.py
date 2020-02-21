# -*- coding: utf-8 -*-

from .context import eatyourlooks

from tests.helpers import *

import unittest


class DocumentExtractionTestSuite(unittest.TestCase):
    """Test cases."""

    def test_get_bounds(self):
        full_api_response = load_api_response_from_file("tests/inputs/parsed-caponata-cropped")
        text_annotation = full_api_response.full_text_annotation


        bounds = eatyourlooks.get_document_block_bounds(text_annotation)
        self.assertEqual(len(bounds), 6)
        # spot check a couple
        self.assertEqual(bounds[0].vertices[0].x, 391)
        self.assertEqual(bounds[5].vertices[0].y, 2399)


if __name__ == '__main__':
    unittest.main()
