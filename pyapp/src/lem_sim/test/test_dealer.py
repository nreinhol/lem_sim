import unittest

from lem_sim import globalmemory as mem
from lem_sim import contract


class DealerTest(unittest.TestCase):

    def test_function_transaction(self):
        variables = mem.Variables('ip')
        agent = variables.agent_pool[0]
        message = 'Bin laepsch!!'

        contract_handler = contract.ContractHandler(variables.web3, 'Inbox.json')
        contract_handler._contract.functions.setMessage(message).transact({'from': agent.account_address, 'gas': 1000000})

        self.assertEqual(message, contract_handler._contract.functions.getMessage().call())
