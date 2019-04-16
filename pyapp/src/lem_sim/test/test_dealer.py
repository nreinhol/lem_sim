import unittest

from lem_sim import communication
from lem_sim import contract

class DealerTest(unittest.TestCase):
    
    def test_connection(self):
        web3 = communication.get_network_connection('ip')
        contract_handler = contract.ContractHandler(web3, 'Inbox.json')
        