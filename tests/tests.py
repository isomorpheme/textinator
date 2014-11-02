import unittest
from textinator import calculate_size


class CalculateSizeTestCase(unittest.TestCase):
    """Tests for calculate_size()"""

    def test_width_no_height(self):
        self.assertEqual(calculate_size((1920, 1080), (20, None)), (20, 11))
        self.assertEqual(calculate_size((500, 1240), (200, None)), (200, 496))

    def test_height_no_width(self):
        self.assertEqual(calculate_size((1024, 768), (None, 413)), (551, 413))
        self.assertEqual(calculate_size((10, 670), (None, 800)), (12, 800))

    def test_height_and_width(self):
        self.assertEqual(calculate_size((500, 600), (42, 612)), (42, 612))

if __name__ == '__main__':
    unittest.main()
