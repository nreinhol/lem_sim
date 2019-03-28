
class Agent():

    def __init__(self, account_address, provider):
        self._account_address = account_address
        self._provider = provider
        self._optimization_problem = None

    @property
    def account_address(self):
        return self._account_address

    @property
    def balance(self):
        return self._provider.eth.getBalance(self.account_address)

    @property
    def optimization_problem(self):
        return self._optimization_problem

    @optimization_problem.setter
    def optimization_problem(self, value):
        self._optimization_problem = value

    def send_transaction(self, receiver_account_address, value):
        self._provider.eth.sendTransaction({'to': receiver_account_address, 'from': self.account_address, 'value': value})
