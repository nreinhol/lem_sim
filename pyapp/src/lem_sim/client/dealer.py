

class Dealer(object):

    def __init__(self, account_address, provider, dealer_contract):
        self._account_address = account_address
        self._provider = provider
        self._dealer_contract = dealer_contract
        self._resource_inventory = None
        self._mkt_prices = None
    
    @property
    def account_address(self):
        return self._account_address

    @property
    def resource_inventory(self):
        return self._resource_inventory

    @resource_inventory.setter
    def resource_inventory(self, value):
        self._resource_inventory = value
    
    def set_mkt_prices(self):
        self._dealer_contract.contract.functions.setMktPrices(self._mkt_prices).transact({'from': self._account_address})
    
    def set_resource_inventory(self, resource_inventory):
        self._dealer_contract.contract.functions.setResourceInventory(self._resource_inventory)

    def get_resource_inventory(self):
        return self._dealer_contract.contract.functions.getResourceInventory().call()
    
    def get_orders(self):
        order_count = self._dealer_contract.contract.functions.order_count().call()

        for order in range(order_count):
            # TODO: process and collect all orders of each account
            pass

    def set_trades(self, account, bundle, bill):
        self._dealer_contract.contract.functions.setTrade(account, bundle, bill).transact({'from': self._account_address})