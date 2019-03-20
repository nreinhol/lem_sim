from lem_sim import communication
from lem_sim import agent


class GlobalVariables():

    def __init__(self, connection):
        self._web3 = communication.get_network_connection(connection)
        self._accounts = self._web3.eth.accounts
        self._agents_list = self.agent_factory()
    
    @property
    def web3(self):
        return self._web3

    @property
    def accounts(self):
        return self._accounts

    @property
    def agents_list(self):
        return self._agents_list
    
    def agent_factory(self):
        agents_list = []
        for account in self._accounts:
            agents_list.append(agent.Agent(account, self._web3))
        return agents_list     