import unittest

from lem_sim import communication


class DealerTest(unittest.TestCase):
    
    def test_connection(self):
        web3 = communication.get_network_connection('ip')
        inbox = web3.eth.contract.Contract('0x2f39b243ce6f1771C5746b5702Dc51Ab1b6D3D14')
        print(inbox)