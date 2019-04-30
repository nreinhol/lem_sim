

class Dealer(object):

    def __init__(self, account_address, provider):
        self._account_address = account_address
        self._provider = provider
        self._resource_inventory = None
    
    @property
    def account_address(self):
        return self._account_address

    @property
    def resource_inventory(self):
        return self._resource_inventory

    @resource_inventory.setter
    def resource_inventory(self, value):
        self._resource_inventory = value