import unittest
import numpy as np

from lem_sim import globalmemory as mem
from lem_sim import utils


class OrdersTest(unittest.TestCase):
    
    def test_get_concatenated_bundles(self):
        orders = utils.Orders('test09')

        # 1st order
        bundle_i = np.array([8, 3])
        bid_i = 6
        indice_i = 0
        # 2nd order
        bundle_j = np.array([2, 3])
        bid_j = 7
        indice_j = 1
        # 3rd order
        bundle_k = np.array([6, 7])
        bid_k = 7
        indice_k = 2

        orders.add_order(bundle_i, bid_i, indice_i)
        orders.add_order(bundle_j, bid_j, indice_j)
        orders.add_order(bundle_k, bid_k, indice_k)

    def test_calculate_trade(self):
        first_order = ['account_1', [8, 3], 6]
        second_order = ['account_1', [2, 9], 3]

        var = mem.Variables('ip')
        dealer = var.dealer
        dealer._mmp_values = np.array([1, 0])
        dealer._order_handler = utils.OrderHandler()
        dealer._order_handler.add_order(0, first_order)
        dealer._order_handler.add_order(1, second_order)
        dealer.set_trade_share()
        orders = dealer._order_handler.get_all_orders()

        trades = []
        for order in orders:
            order.calculate_trade()
            trades.append(order._trade)
        
        print(trades)

