import numpy as np

from lem_sim import communication
from lem_sim import client
from lem_sim import contract
from lem_sim import linearoptimization as lp

''' Definition of the Central Optimization Problem '''
TARGET_COEFS = np.array([-1, -2, -1, -3])  # cost vectors (d)
INDIVIDUAL_RESOURCES = np.array([4, 9])  # individual resources (n)
INDIVIDUAL_COEFS = np.array([[2, 1, 0, 0], [0, 0, 2, 3]])  # individual coefficients(N)
SHARED_RESOURCES = np.array([8, 5])  # shared resources (c)
SHARED_COEFS = np.array([[1, 3, 2, 1], [1, 1, 1, 1]])  # shared coefficients (C)


class Variables(object):

    def __init__(self, connection):
        self._central_problem = lp.OptimizationProblem(TARGET_COEFS, INDIVIDUAL_RESOURCES, INDIVIDUAL_COEFS, SHARED_RESOURCES, SHARED_COEFS)
        self._web3 = communication.get_network_connection(connection)
        self._dealer_contract = contract.ContractHandler(self._web3, 'Dealer.json')
        self._accounts = self._web3.eth.accounts
        self._dealer = client.Dealer(self._accounts.pop(0), self._web3, self._dealer_contract, self._central_problem.shared_resources.size)
        self._agent_pool = [client.Agent(number, account, self._web3, self._dealer_contract) for number, account in enumerate(self._accounts, 1)]
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

    @property
    def central_problem(self):
        return self._central_problem
