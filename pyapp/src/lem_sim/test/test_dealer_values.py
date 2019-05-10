import unittest
import numpy as np

from lem_sim import utils
from lem_sim import globalmemory as mem


class DealerValuesTest(unittest.TestCase):

    def test_shift_decimal_places(self):
        bundle = [3.55, 4.66]
        value = 3

        int_bundle = utils.shift_decimal_right(bundle)
        float_bundle = utils.shift_decimal_left(int_bundle)

        int_value = utils.shift_decimal_right(value)
        float_value = utils.shift_decimal_left(int_value)

        self.assertEqual(bundle, float_bundle)
        self.assertEqual(int_bundle, [355, 466])

        self.assertEqual(value, float_value)
        self.assertEqual(int_value, 300)

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

    def test_create_trades(self):
        first_order = ['account_1', [8, 3], 6]
        second_order = ['account_1', [2, 9], 3]
        third_order = ['account_2', [1, 4], 7]
        fourth_order = ['account_1', [5, 6], 4]

        var = mem.Variables('ip')
        dealer = var.dealer
        dealer._mmp_values = np.array([1, 0, 1, 1])
        dealer._order_handler = utils.OrderHandler()
        dealer._order_handler.add_order(0, first_order)
        dealer._order_handler.add_order(1, second_order)
        dealer._order_handler.add_order(2, third_order)
        dealer._order_handler.add_order(3, fourth_order)
        dealer.set_trade_share()
