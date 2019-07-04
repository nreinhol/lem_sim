import numpy as np
from scipy.optimize import linprog
import math

from lem_sim import utils


class Agent(object):

    def __init__(self, agent_number, account_address, web3, dealer_contract):
        self._name = 'AGENT{}'.format(agent_number)
        self._account_address = account_address
        self._web3 = web3
        self._dealer_contract = dealer_contract
        self._optimization_problem = None
        self._bundle_set = None
        self._bid = None
        self._bill = None
        self._mkt_prices = None
        self._trade = None
        self._objective = None
        self._wealth = None
        self._accept_trade = None

    ''' getter and setter of class attributes '''

    @property
    def name(self):
        return self._name

    @property
    def objective(self):
        return self._objective

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
        balance = self._web3.eth.getBalance(self._account_address)
        return float(utils.from_wei_to_ether(balance))

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
        self._objective = self._optimization_problem.solve().fun  # set initial objective
        self._wealth = self.balance + abs(self._objective)  # set initial wealth

    ''' functions for contract communication '''

    def accept_trade(self):
        trade = self._dealer_contract.contract.functions.acceptTrade(self._accept_trade).call({'from': self._account_address})
        self._trade = utils.prepare_for_storing(trade)
        self._dealer_contract.contract.functions.acceptTrade(self._accept_trade).transact({'from': self._account_address})

    def set_order(self):
        bundle_set = utils.prepare_for_sending(self._bundle_set)
        bid = utils.prepare_for_sending(self._bid)
        prepayment = utils.from_ether_to_wei(self._bid)
        self._dealer_contract.contract.functions.setOrder(bundle_set, bid, prepayment).transact({'from': self._account_address, 'value': prepayment})

    def get_mkt_prices(self):
        mkt_prices = self._dealer_contract.contract.functions.getMktPrices().call()
        self._mkt_prices = utils.prepare_for_storing(mkt_prices)

    ''' functions to determine inner class attributes '''

    def determine_bundle_attributes(self):
        result = solve_bundle_determination(self._optimization_problem, self._mkt_prices)
        self._bundle_set = result.x
        self._bid = self._objective - result.fun

    def get_mmp_attributes(self):
        mmp_attributes = self._dealer_contract.contract.functions.getMMPAttributes().call()
        mmp_values = utils.prepare_for_storing(mmp_attributes[0])
        mmp_duals = utils.prepare_for_storing(mmp_attributes[1])
        mmp_target_coefs = utils.prepare_for_storing(mmp_attributes[2])
        mmp_bounds = utils.prepare_for_storing(mmp_attributes[3])

        return mmp_values, mmp_duals, mmp_target_coefs, mmp_bounds

    def verify_strong_duality(self):
        mmp_values, mmp_duals, mmp_target_coefs, mmp_bounds = self.get_mmp_attributes()
        primal_bound = (-np.sum(mmp_values * mmp_target_coefs))
        dual_bound = np.sum(mmp_duals * mmp_bounds)
        primal_bound = math.floor(primal_bound * 10) / 10
        dual_bound = math.floor(dual_bound * 10) / 10

        if primal_bound == dual_bound:
            self._accept_trade = True
        else:
            self._accept_trade = False

    def add_trade_to_shared_resources(self):
        # only add trade to shared resources and recalculate objective and bill if trade accepted
        if(self._accept_trade):
            self._optimization_problem.shared_resources = np.add(self._optimization_problem.shared_resources, self._trade)
            self._objective = self._optimization_problem.solve().fun  # calculate new objective after getting new shared resources
            self._wealth = self.balance + abs(self._objective)  # calculate new wealth after new objective calculation

    def __str__(self):
        class_str = '\n{}\naccount: {}\nbalance: {} ether\nobjective: {}\nwealth: {}\norder: {}\nbid: {} ether\ntrade: {}\ntrade accepted: {} \nallocation: {}'.format(
            self._name,
            self._account_address,
            self.balance,
            self._objective,
            self._wealth,
            self._bundle_set,
            self._bid,
            self._trade,
            self._accept_trade,
            self.optimization_problem.shared_resources
        )

        return class_str


def solve_bundle_determination(optimization_problem, mkt_prices):
        bundle_target_coefs = np.concatenate((optimization_problem.target_coefs, mkt_prices))

        bundle_individual_coefs = np.concatenate((optimization_problem.individual_coefs, np.zeros(optimization_problem.individual_coefs.shape)), axis=1)
        bundle_shared_coefs = np.concatenate((optimization_problem.shared_coefs, np.identity(mkt_prices.size, dtype=float) * (-1)), axis=1)

        bundle_var_geq_zero_constraint = np.concatenate((np.identity(mkt_prices.size) * (-1), np.zeros(optimization_problem.shared_coefs.shape)), axis=1)
        bundle_var_geq_zero_bound = np.zeros(mkt_prices.size)

        bundle_coefs = np.concatenate((bundle_individual_coefs, bundle_shared_coefs, bundle_var_geq_zero_constraint))
        bundle_resources = np.concatenate((optimization_problem.individual_resources, optimization_problem.shared_resources, bundle_var_geq_zero_bound))

        result = linprog(bundle_target_coefs, bundle_coefs, bundle_resources)
        result.x = result.x[- mkt_prices.size:]  # remove not bundle coefficients

        return result
