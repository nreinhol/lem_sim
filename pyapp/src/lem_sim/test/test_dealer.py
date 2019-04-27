import unittest
import numpy as np

from lem_sim import contract
from lem_sim import globalmemory as mem
from lem_sim import linearoptimization as lp


class DealerTest(unittest.TestCase):

    def test_owner(self):
        variables = mem.Variables('ip')
        owner = variables.dealer_contract.contract.functions.getOwner().call()
        self.assertEqual(owner, variables.dealer)
    
    def test_mkt_prices(self):
        variables = mem.Variables('ip')
        mkt_prices = [3, 4]
        variables.dealer_contract.contract.functions.setMktPrices(mkt_prices).transact({'from': variables.dealer, 'gas': 1000000})
        contract_mkt_prices = variables.dealer_contract.contract.functions.getMktPrices().call()
        self.assertEqual(mkt_prices, contract_mkt_prices)
    
    def test_order_count(self):
        variables = mem.Variables('ip')
        agent = variables.agent_pool[0]
        variables.dealer_contract.contract.functions.setOrderCount().transact({'from': agent.account_address})
        count = variables.dealer_contract.contract.functions.getOrderCount().transact({'from': agent.account_address})
        print(count)
        
        