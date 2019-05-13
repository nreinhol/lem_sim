import unittest

from lem_sim import globalmemory as mem


class DealerEventsTest(unittest.TestCase):

    def test_received_order(self):

        var = mem.Variables('ip')

        myfilter = var.dealer._dealer_contract.contract.events.ReceivedOrder.createFilter(fromBlock=0, toBlock='latest')
        eventlist = myfilter.get_all_entries()
        for entry in eventlist:
            print(entry['args'])
