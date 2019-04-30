import unittest

from lem_sim import globalmemory as mem


class DealerContractTest(unittest.TestCase):

    def test_owner(self):
        var = mem.Variables('ip')
        owner = var.dealer_contract.contract.functions.getOwner().call()
        self.assertEqual(owner, var.dealer.account_address)

    def test_mkt_prices(self):
        var = mem.Variables('ip')
        agent = var.agent_pool[0]
        dealer = var.dealer

        # set mkt price vector
        dealer.mkt_prices = [3, 4]
        # set mkt prices in contract
        dealer.set_mkt_prices()
        # get mkt prices from contract
        contract_mkt_prices = agent.get_mkt_prices()

        self.assertEqual(dealer.mkt_prices, contract_mkt_prices)

    def test_order(self):
        var = mem.Variables('ip')
        agent = var.agent_pool[0]
        dealer = var.dealer

        # set a bundle
        agent.bundle_set = [8, 5]
        # set bid
        agent.bid = 6
        # set order transaction
        agent.set_order()
        # get latest order
        order = dealer.get_orders()

        self.assertEqual(order[0], agent.account_address)
        self.assertEqual(order[1], agent.bundle_set)
        self.assertEqual(order[2], agent.bid)

    def test_trade(self):
        var = mem.Variables('ip')
        agent = var.agent_pool[0]
        dealer = var.dealer

        # send trade tansaction
        dealer.set_trades(agent.account_address, [1, 2], 1000)

        # get bill from contract
        agent.get_bill()
        # get trade vom contract
        trade = agent.get_trade()

        self.assertEqual(trade, [1, 2])
