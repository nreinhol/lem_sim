import numpy as np
from cvxopt import matrix, solvers

from lem_sim import utils


class Dealer(object):

    def __init__(self, account_address, provider, dealer_contract, shared_resource_size):
        self._account_address = account_address
        self._provider = provider
        self._dealer_contract = dealer_contract
        self._resource_inventory = None
        self._trade = None
        self._shared_resource_size = shared_resource_size
        self._mkt_prices = np.zeros(self._shared_resource_size)
        self._order_handler = None

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
        mkt_prices = utils.prepare_for_sending(self._mkt_prices)
        self._dealer_contract.contract.functions.setMktPrices(mkt_prices).transact({'from': self._account_address})

    def set_resource_inventory(self):
        self._dealer_contract.contract.functions.setResourceInventory(self._resource_inventory)

    def get_resource_inventory(self):
        return self._dealer_contract.contract.functions.getResourceInventory().call()

    def get_order_indices(self):
        return list(filter(None, self._dealer_contract.contract.functions.getOrderIndices().call()))

    def get_orders(self):
        self._order_handler = utils.OrderHandler()
        order_indices = self.get_order_indices()

        # get all orders from contract and store in order handler
        for order_id in order_indices:
            order = self._dealer_contract.contract.functions.getOrder(order_id).call()
            self._order_handler.add_order(order_id, order)

    def delete_order(self):
        settled_orders = self.get_settled_order_indices()
        for order_id in settled_orders:
            self._dealer_contract.contract.functions.deleteOrder(order_id).transact({'from': self._account_address, 'gas': 300000})

    def set_trades(self):
        self.set_trade_share()
        self.initiate_trade_calculation()
        self.initiate_bill_calculation()
        for order in self._order_handler.get_all_orders():
            account, trade, bill = order.get_trade_information()
            bill = utils.from_ether_to_wei(bill)
            self._dealer_contract.contract.functions.setTrade(account, trade, bill).transact({'from': self._account_address})

    def create_mmp(self):
        bundles = [order.get_concatenated_bundles() for order in self._order_handler.get_all_orders()]
        bids = [order.get_concatenated_bids() for order in self._order_handler.get_all_orders()]

        try:
            TARGET_COEFS = np.hstack(bids) * (-1)  # create target coef vector

            self._mmp_amount_variables = np.size(TARGET_COEFS)  # set amount of variables
            mmp_coefs = np.hstack(bundles)
            var_leq_one_coefs = np.identity(self._mmp_amount_variables, dtype=float)  # create constraint matrix for y<=1
            var_geq_zero_coefs = np.identity(self._mmp_amount_variables, dtype=float) * (-1)  # create constraint matrix for y>=0
            mmp_bounds = self._resource_inventory
            var_leq_one_bounds = np.ones(self._mmp_amount_variables, dtype=float)
            var_geq_zero_bounds = np.zeros(self._mmp_amount_variables, dtype=float)

            CONSTRAINT_COEFS = np.concatenate((mmp_coefs, var_leq_one_coefs, var_geq_zero_coefs), axis=0)  # create final constraint matrix
            CONSTRAINT_BOUNDS = np.concatenate((mmp_bounds, var_leq_one_bounds, var_geq_zero_bounds))  # create final bounds matrix

            self._mmp_constraint_coefs = matrix(CONSTRAINT_COEFS)
            self._mmp_constraint_bounds = matrix(CONSTRAINT_BOUNDS)
            self._mmp_target_coefs = matrix(TARGET_COEFS)

        except ValueError as error:
            print('Creation of MMP failed!')
            print(error)

    def solve_mmp(self):
        solvers.options['show_progress'] = False
        sol = solvers.lp(self._mmp_target_coefs, self._mmp_constraint_coefs, self._mmp_constraint_bounds)
        self._mmp_values = np.array([float('%.2f' % (sol['x'][i])) for i in range(self._mmp_amount_variables)])
        self._mkt_prices = np.array([float('%.2f' % (sol['z'][i])) for i in range(self._shared_resource_size)])

    def set_trade_share(self):
        amount_orders = [order.amount_orders for order in self._order_handler.get_all_orders()]
        trade_share = self._mmp_values
        for amount, orders in zip(amount_orders, self._order_handler.get_all_orders()):
            orders.trade_share = trade_share[0:amount]
            trade_share = trade_share[amount:]

    def initiate_trade_calculation(self):
        for order in self._order_handler.get_all_orders():
            order.calculate_trade()

    def initiate_bill_calculation(self):
        for order in self._order_handler.get_all_orders():
            order.calculate_bill(self._mkt_prices)

    def get_settled_order_indices(self):
        settled_orders = []

        for order in self._order_handler.get_all_orders():
            indice_of_trade_shares_not_zero = (order.trade_share.nonzero()[0].tolist())
            indice_of_settled_orders = [order.indices[index] for index in indice_of_trade_shares_not_zero]
            settled_orders += indice_of_settled_orders

        return settled_orders

    def calculate_resource_inventory(self):
        self._trade = sum([order.trade for order in self._order_handler.get_all_orders()])
        self._resource_inventory = utils.truncate_values_of_array(self._resource_inventory - self._trade)

    def __str__(self):
        class_str = '\nDEALER\naccount: {}\ndealer inventory: {}\ndealer trade: {}\nmarket price: {}'.format(
            self._account_address,
            self._resource_inventory,
            self._trade,
            self._mkt_prices,
        )
        return class_str
