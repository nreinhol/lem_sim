import unittest
import numpy as np

from lem_sim import contract
from lem_sim import globalmemory as mem
from lem_sim import linearoptimization as lp


class DealerTest(unittest.TestCase):

    def test_inbox_contract(self):
        variables = mem.Variables('ip')
        agent = variables.agent_pool[0]
        message = 'Bin laepsch!!'

        contract_handler = contract.ContractHandler(variables.web3, 'Inbox.json')
        contract_handler._contract.functions.setMessage(message).transact({'from': agent.account_address, 'gas': 1000000})

        self.assertEqual(message, contract_handler.contract.functions.getMessage().call())

    def test_dealer_contract(self):
        TARGET_COEFS = np.array([-1, -2, -1, -3])  # cost vectors (d)
        INDIVIDUAL_RESOURCES = np.array([4, 9])  # individual resources (n)
        INDIVIDUAL_COEFS = np.array([[2, 1, 0, 0], [0, 0, 2, 3]])  # individual coefficients(N)
        SHARED_RESOURCES = np.array([8, 5])  # shared resources (c)
        SHARED_COEFS = np.array([[1, 3, 2, 1], [1, 1, 1, 1]])  # shared coefficients (C)
        

        variables = mem.Variables('ip')
        central_problem = lp.OptimizationProblem(TARGET_COEFS, INDIVIDUAL_RESOURCES, INDIVIDUAL_COEFS, SHARED_RESOURCES, SHARED_COEFS)
        lp.decompose(central_problem, variables)
        
        agent = variables.agent_pool[0]
        order = agent.bundle_set * 100000 # five places after decimal
        order = [int(i) for i in order]
        
        variables.dealer_contract.contract.functions.addOrder(order).transact({'from': agent.account_address, 'gas': 1000000})
        response = variables.dealer_contract.contract.functions.getOrders(agent.account_address).call()
        