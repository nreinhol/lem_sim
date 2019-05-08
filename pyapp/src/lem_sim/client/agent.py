import numpy as np
from scipy.optimize import linprog

from lem_sim import utils


class Agent(object):

    def __init__(self, account_address, provider, dealer_contract):
        self._account_address = account_address
        self._provider = provider
        self._dealer_contract = dealer_contract
        self._optimization_problem = None
        self._bundle_set = None
        self._bid = None
        self._bill = None
        self._mkt_prices = None
        self._trade = None

    @property
    def bill(self):
        return self._bill

    @property
    def mkt_prices(self):
        return self._mkt_prices

    @property
    def trade(self):
        return self._trade

    @property
    def account_address(self):
        return self._account_address

    @property
    def balance(self):
        return self._provider.eth.getBalance(self._account_address)

    @property
    def bundle_set(self):
        return self._bundle_set

    @bundle_set.setter
    def bundle_set(self, value):
        self._bundle_set = value

    @property
    def bid(self):
        return self._bid

    @bid.setter
    def bid(self, value):
        self._bid = value

    @property
    def optimization_problem(self):
        return self._optimization_problem

    @optimization_problem.setter
    def optimization_problem(self, value):
        self._optimization_problem = value

    def determine_bundle_attributes(self):
        result = solve_bundle_determination(self._optimization_problem, self._mkt_prices)
        self._bundle_set = result.x
        self._bid = abs(self._optimization_problem.solve().fun - result.fun)

    def get_mkt_prices(self):
        mkt_prices = self._dealer_contract.contract.functions.getMktPrices().call()
        self._mkt_prices = utils.prepare_for_storing(mkt_prices)

    def get_bill(self):
        bill = self._dealer_contract.contract.functions.getBill().call({'from': self._account_address})
        self._bill = utils.prepare_for_storing(bill)

    def get_trade(self):
        bill = utils.prepare_for_sending(self._bill)
        trade = self._dealer_contract.contract.functions.getTrade().call({'from': self._account_address, 'value': bill})
        self._trade = utils.prepare_for_storing(trade)
        self._dealer_contract.contract.functions.getTrade().transact({'from': self._account_address, 'value': bill})

    def set_order(self):
        if(np.array_equal(self._bundle_set, np.array([0, 0], dtype=float))):
            pass
        else:
            bundle_set = utils.prepare_for_sending(self._bundle_set)
            bid = utils.prepare_for_sending(self._bid)
            self._dealer_contract.contract.functions.setOrder(bundle_set, bid).transact({'from': self._account_address})

    def add_trade_to_shared_resources(self):
        self._optimization_problem.shared_resources = np.add(self._optimization_problem.shared_resources, self._trade)
    
    def __str__(self):
        class_str = '\naccount: {}\norder: {}\nbid: {}\ntrade: {}\nbill: {}\nallocation: {}'.format(
            self._account_address,
            self._bundle_set,
            self._bid,
            self._trade,
            self._bill,
            self.optimization_problem.shared_resources
            )
        return class_str

def solve_bundle_determination(optimization_problem, mkt_prices):
        bundle_target_coefs = np.concatenate((optimization_problem.target_coefs, mkt_prices))
        bundle_individual_coefs = np.concatenate((optimization_problem.individual_coefs, np.zeros(optimization_problem.individual_coefs.shape)), axis=1)
        bundle_shared_coefs = np.concatenate((optimization_problem.shared_coefs, np.identity(mkt_prices.size, dtype=float) * (-1)), axis=1)

        bundle_coefs = np.concatenate((bundle_individual_coefs, bundle_shared_coefs))
        bundle_resources = np.concatenate((optimization_problem.individual_resources, optimization_problem.shared_resources))

        result = linprog(bundle_target_coefs, bundle_coefs, bundle_resources)
        result.x = result.x[- mkt_prices.size:]  # remove not bundle coefficients

        return result
