import unittest
import numpy as np

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
    
    def test_order_pool(self):
        order_pool = utils.OrderPool()
        
        account = 'nik09'
        bundle_i = [80000000000, 30000000000]
        bid_i = 60000000000
        
        order_id = 0

        order = [account, bundle_i, bid_i]

