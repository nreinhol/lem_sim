import unittest
import numpy as np

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

    def test_prepare_for_sending(self):
        array = np.array([1, 2, 3])
        value = 1.56
        prepared_array = utils.prepare_for_sending(array)
        prepared_value = utils.prepare_for_sending(value)

        self.assertIsInstance(prepared_array, list)
        self.assertIsInstance(prepared_array[0], int)
        self.assertIsInstance(prepared_value, int)

    def test_prepare_for_storing(self):
        received_list = [100, 200, 300]
        received_value = 190000
        prepared_list = utils.prepare_for_storing(received_list)
        prepared_value = utils.prepare_for_storing(received_value)

        self.assertIsInstance(prepared_list, np.ndarray)
        self.assertIsInstance(prepared_list[0], float)
        self.assertIsInstance(prepared_value, float)
