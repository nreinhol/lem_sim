
class Agent():

    def __init__(self, account_address, provider):
        self._account_address = account_address
        self._provider = provider

    @property
    def account_address(self):
        return self._account_address

    @property
    def balance(self):
        return self._provider.eth.getBalance(self.account_address)

    def send_transaction(self, receiver_account_address, value):
        self._provider.eth.sendTransaction({'to': receiver_account_address, 'from': self.account_address, 'value': value})
