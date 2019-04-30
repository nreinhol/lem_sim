from lem_sim import communication
from lem_sim import client
from lem_sim import contract


class Variables(object):

    def __init__(self, connection):
        self._web3 = communication.get_network_connection(connection)
        self._dealer_contract = contract.ContractHandler(self._web3, 'Dealer.json')
        self._accounts = self._web3.eth.accounts
        self._dealer = client.Dealer(self._accounts.pop(0), self._web3, self._dealer_contract)
        self._agent_pool = [client.Agent(account, self._web3, self._dealer_contract) for account in self._accounts]
        self._amount_agents = len(self._agent_pool)

    @property
    def web3(self):
        return self._web3

    @property
    def accounts(self):
        return self._accounts

    @property
    def agent_pool(self):
        return self._agent_pool

    @property
    def amount_agents(self):
        return self._amount_agents

    @property
    def dealer_contract(self):
        return self._dealer_contract

    @property
    def dealer(self):
        return self._dealer
