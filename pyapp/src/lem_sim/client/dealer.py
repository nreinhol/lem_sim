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

        self._mmp_target_coefs = None
        self._mmp_constraint_coefs = None
        self._mmp_constraint_bounds = None
        self._mmp_amount_variables = None
        self._mmp_values = None

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

    def create_mmp(self):
        bundles = [order.get_concatenated_bundles() for order in self._order_pool.get_all_orders()]
        bids = [order.get_concatenated_bids() for order in self._order_pool.get_all_orders()]

        try:
            TARGET_COEFS = np.hstack(bids) * (-1)  # create target coef vector 
            VARIABLE_LEQ_CONSTRAINT = np.identity(self._resource_inventory.size, dtype=float)  # create constraint matrix for y<=1
            CONSTRAINT_COEFS = np.concatenate((np.hstack(bundles), VARIABLE_LEQ_CONSTRAINT), axis=0)  # create final constraint matrix
            self._mmp_amount_variables = np.size(CONSTRAINT_COEFS, 1)  # set amount of variables 
            CONSTRAINT_BOUNDS = np.concatenate((self._resource_inventory, np.ones(self._mmp_amount_variables, dtype=float)))

            self._mmp_constraint_coefs = matrix(CONSTRAINT_COEFS)
            self._mmp_constraint_bounds = matrix(CONSTRAINT_BOUNDS)
            self._mmp_target_coefs = matrix(TARGET_COEFS)

        except ValueError as error:
            print('Creation of MMP failed!')
            print(error)

    def solve_mmp(self):
        solvers.options['show_progress'] = False
        sol = solvers.lp(self._mmp_target_coefs, self._mmp_constraint_coefs, self._mmp_constraint_bounds)

        self._mmp_values = [float('%.5f' % (sol['x'][i])) for i in range(self._mmp_amount_variables)]
        self._mkt_prices = [float('%.5f' % (sol['z'][i])) for i in range(self._mmp_amount_variables)]

    def set_trade_share(self):
        amount_orders = [order.amount_orders for order in self._order_pool.get_all_orders()]
        trade_share = self._mmp_values
        for amount, orders in zip(amount_orders, self._order_pool.get_all_orders()):
            orders.trade_share = trade_share[0:amount]
            trade_share = trade_share[amount:]
    
    def get_settled_order_indices(self):
        settled_orders = []
        
        for order in self._order_pool.get_all_orders():
            indice_of_trade_shares_not_zero = (order.trade_share.nonzero()[0].tolist())
            indice_of_settled_orders = [order.indices[index] for index in indice_of_trade_shares_not_zero]
            settled_orders += indice_of_settled_orders
        
        return settled_orders
