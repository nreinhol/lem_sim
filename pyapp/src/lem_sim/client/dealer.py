import numpy as np

from lem_sim import utils


class Dealer(object):

    def __init__(self, account_address, provider, dealer_contract, shared_resource_size):
        self._account_address = account_address
        self._provider = provider
        self._dealer_contract = dealer_contract
        self._resource_inventory = None
        self._mkt_prices = np.zeros(shared_resource_size)
        self._orders = {}

    @property
    def account_address(self):
        return self._account_address

    @property
    def mkt_prices(self):
        return self._mkt_prices

    @mkt_prices.setter
    def mkt_prices(self, value):
        self._mkt_prices = value

    @property
    def resource_inventory(self):
        return self._resource_inventory

    @resource_inventory.setter
    def resource_inventory(self, value):
        self._resource_inventory = value

    def set_mkt_prices(self):
        mkt_prices = utils.shift_decimal_right(self._mkt_prices.tolist())
        self._dealer_contract.contract.functions.setMktPrices(mkt_prices).transact({'from': self._account_address})

    def set_resource_inventory(self):
        self._dealer_contract.contract.functions.setResourceInventory(self._resource_inventory)

    def get_resource_inventory(self):
        return self._dealer_contract.contract.functions.getResourceInventory().call()

    def get_orders(self):
        order_count = self._dealer_contract.contract.functions.order_count().call()

        # get all orders
        for order in range(order_count):
            order = self._dealer_contract.contract.functions.getOrder(order).call()
            account = order.pop(0)
            order_dict = {}
            
            for index, element in enumerate(order):
                order_dict[index] = utils.prepare_for_storing(element)

            if account in self._orders.keys():
                self._orders[account].append(order_dict)
            else:
                self._orders[account] = [order_dict]
        
        print(self._orders)

    def set_trades(self, account, bundle, bill):
        self._dealer_contract.contract.functions.setTrade(account, bundle, bill).transact({'from': self._account_address})
