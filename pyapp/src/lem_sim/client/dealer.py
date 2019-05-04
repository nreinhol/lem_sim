import numpy as np
from cvxopt import matrix, solvers
from lem_sim import utils


class Dealer(object):

    def __init__(self, account_address, provider, dealer_contract, shared_resource_size):
        self._account_address = account_address
        self._provider = provider
        self._dealer_contract = dealer_contract
        self._resource_inventory = None
        self._mkt_prices = np.zeros(shared_resource_size)
        self._order_pool = utils.OrderPool()

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
        for order_id, order in enumerate(range(order_count)):
            order = self._dealer_contract.contract.functions.getOrder(order).call()
            self._order_pool.add_order(order_id, order)

    def set_trades(self, account, bundle, bill):
        self._dealer_contract.contract.functions.setTrade(account, bundle, bill).transact({'from': self._account_address})

    def solve_mmp(self):
        bundles = [order.get_concatenated_bundles() for order in self._order_pool.get_all_orders()]
        bids = [order.get_concatenated_bids() for order in self._order_pool.get_all_orders()]
        
        TARGET_COEFS = np.hstack(bids) * (-1)
        VARIABLE_LEQ_CONSTRAINT = np.identity(self._resource_inventory.size, dtype=float)
        CONSTRAINT_COEFS = np.concatenate((np.hstack(bundles), VARIABLE_LEQ_CONSTRAINT), axis=0) 
        AMOUNT_OF_VARIABLES = np.size(CONSTRAINT_COEFS, 1)
        CONSTRAINT_BOUNDS = np.concatenate((self._resource_inventory, np.ones(AMOUNT_OF_VARIABLES, dtype=float))) 

        A = matrix(CONSTRAINT_COEFS)
        b = matrix(CONSTRAINT_BOUNDS)
        c = matrix(TARGET_COEFS)

        print(A)
        print(b)
        print(c)
        # solvers.options['show_progress'] = False
        sol = solvers.lp(c, A, b)

        y_1 = float('%.5f' % (sol['x'][0]))
        y_2 = float('%.5f' % (sol['x'][1]))
        mkt_price_w1 = float('%.5f' % (sol['z'][0]))
        mkt_price_w2 = float('%.5f' % (sol['z'][1]))
        
        print(y_1, y_2)
        print(mkt_price_w1, mkt_price_w2)
        
        

        
        