import unittest

from lem_sim import utils


class DealerValuesTest(unittest.TestCase):

    def test_shift_decimal_places(self):
        bundle = [3.555, 4.666]
        value = 3

        int_bundle = utils.shift_decimal_right(bundle)
        float_bundle = utils.shift_decimal_left(int_bundle)

        int_value = utils.shift_decimal_right(value)
        float_value = utils.shift_decimal_left(int_value)

        self.assertEqual(bundle, float_bundle)
        self.assertEqual(int_bundle, [35550000000, 46660000000])

        self.assertEqual(value, float_value)
        self.assertEqual(int_value, 30000000000)
