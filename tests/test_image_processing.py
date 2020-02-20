# -*- coding: utf-8 -*-

from .context import eatyourlooks

import unittest


class ImageProcessingTestSuite(unittest.TestCase):
    """Test cases."""

    def test_parse(self):
        self.assertFalse(eatyourlooks.parse_image_for_text(None, None))


if __name__ == '__main__':
    unittest.main()
