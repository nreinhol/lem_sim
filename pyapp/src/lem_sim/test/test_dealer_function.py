import unittest
import numpy as np

from lem_sim import globalmemory as mem


class DealerFunctionsTest(unittest.TestCase):

    def test_owner(self):
        var = mem.Variables('ip')
        owner = var.dealer_contract.contract.functions.getOwner().call()
        self.assertEqual(owner, var.dealer.account_address)

    def test_mkt_prices(self):
        var = mem.Variables('ip')
        agent = var.agent_pool[0]
        dealer = var.dealer

        # set mkt price vector
        dealer.mkt_prices = np.array([3, 4])
        # set mkt prices in contract
        dealer.set_mkt_prices()
        # get mkt prices from contract
        agent.get_mkt_prices()

        self.assertTrue(np.array_equal(dealer.mkt_prices, agent.mkt_prices))
