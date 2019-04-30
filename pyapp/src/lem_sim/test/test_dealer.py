import unittest
import numpy as np

from lem_sim import contract
from lem_sim import globalmemory as mem
from lem_sim import linearoptimization as lp


class DealerTest(unittest.TestCase):

    def test_owner(self):
        variables = mem.Variables('ip')
        owner = variables.dealer_contract.contract.functions.getOwner().call()
        self.assertEqual(owner, variables.dealer.account_address)
    
    def test_mkt_prices(self):
        variables = mem.Variables('ip')
        mkt_prices = [3, 4]
        dealer = variables.dealer.account_address
        
        # send mkt prices transaction - only possible from dealer account
        variables.dealer_contract.contract.functions.setMktPrices(mkt_prices).transact({'from': dealer})
        # get mkt prices from contract 
        contract_mkt_prices = variables.dealer_contract.contract.functions.getMktPrices().call()
        
        self.assertEqual(mkt_prices, contract_mkt_prices)

    def test_order(self):
        variables = mem.Variables('ip')
        agent = variables.agent_pool[0] 
        bundle = [8, 3]
        bid = 6

        # send order transaction
        variables.dealer_contract.contract.functions.setOrder(bundle, bid).transact({'from': agent.account_address})
        # get order count
        order_count = variables.dealer_contract.contract.functions.order_count().call()
        # get latest order 
        order = variables.dealer_contract.contract.functions.getOrder(order_count - 1).call()
        
        self.assertEqual(order[0], agent.account_address)
        self.assertEqual(order[1], bundle)
        self.assertEqual(order[2], bid)

    def test_trade(self):
        variables = mem.Variables('ip')
        agent = variables.agent_pool[0]
        dealer = variables.dealer.account_address

        # define a trade
        bundle = [1, 2]
        payment = 1000
        account = agent.account_address

        # send trade tansaction 
        variables.dealer_contract.contract.functions.setTrade(account, bundle, payment).transact({'from': dealer})
        trade = variables.dealer_contract.contract.functions.getTrade().call({'from': account, 'value': payment})
        print(trade)