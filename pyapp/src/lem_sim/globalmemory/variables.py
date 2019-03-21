from lem_sim import communication
from lem_sim import agent


class Variables():

    def __init__(self, connection):
        self._web3 = communication.get_network_connection(connection)
        self._accounts = self._web3.eth.accounts
        self._agent_pool = self.agent_factory()
    
    @property
    def web3(self):
        return self._web3

    @property
    def accounts(self):
        return self._accounts

    @property
    def agent_pool(self):
        return self._agent_pool
    
    def agent_factory(self):
        agent_pool = []
        for account in self._accounts:
            agent_pool.append(agent.Agent(account, self._web3))
        return agent_pool     
