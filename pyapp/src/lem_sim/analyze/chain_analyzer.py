from lem_sim import communication
from lem_sim import contract


class ChainAnalyzer(object):

    def __init__(self, connection):
        self._web3 = communication.get_network_connection(connection)
        self._dealer_contract = contract.ContractHandler(self._web3, 'Dealer.json')

    def filter_received_order_event(self, from_block, to_block):
        event_filter = self._dealer_contract.contract.events.ReceivedOrder.createFilter(fromBlock=from_block, toBlock=to_block)
        return event_filter.get_all_entries()

    def filter_stored_trade_event(self, from_block, to_block):
        event_filter = self._dealer_contract.contract.events.StoredTrade.createFilter(fromBlock=from_block, toBlock=to_block)
        return event_filter.get_all_entries()
