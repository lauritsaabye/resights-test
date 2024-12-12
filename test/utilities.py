import unittest
from lib.utilities import convert_to_bounds


class TestConvertToBounds(unittest.TestCase):
    def test_range_with_hyphen(self):
        result = convert_to_bounds("50-67%")
        self.assertEqual(result, (0.5, 0.67))

    def test_single_percentage(self):
        result = convert_to_bounds("100%")
        self.assertEqual(result, (1.0, 1.0))

    def test_less_than_percentage(self):
        result = convert_to_bounds("<5%")
        self.assertEqual(result, (0, 0.05))

    def test_edge_case_empty_input(self):
        with self.assertRaises(ValueError):
            convert_to_bounds("")

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            convert_to_bounds("50-67-80%")
