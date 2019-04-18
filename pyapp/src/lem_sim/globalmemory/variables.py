from lem_sim import communication
from lem_sim import agent
from lem_sim import contract


class Variables(object):

    def __init__(self, connection):
        self._web3 = communication.get_network_connection(connection)
        self._accounts = self._web3.eth.accounts
        self._agent_pool = [agent.Agent(account, self._web3)for account in self._accounts]
        self._amount_agents = len(self._agent_pool)
        self._dealer_contract = contract.ContractHandler(self._web3, 'Dealer.json')

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