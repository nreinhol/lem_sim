import numpy as np

from lem_sim import utils


class OrderHandler(object):

    def __init__(self):
        self._pool = {}

    def add_order(self, order_id, order):
        account = order[0]
        bundle = utils.prepare_for_storing(order[1])
        bid = utils.prepare_for_storing(order[2])

        if account in self._pool.keys():
            self._pool[account].add_order(bundle, bid, order_id)
        else:
            self._pool[account] = Orders(account)
            self._pool[account].add_order(bundle, bid, order_id)
 
    def get_all_accounts(self):
        return self._pool.keys()

    def get_orders_of_account(self, account):
        return self._pool[account]

    def get_all_orders(self):
        return [self._pool[account] for account in self._pool.keys()]   


class Orders(object):

    def __init__(self, account):
        self._account = account
        self._bundles = []
        self._bids = []
        self._indices = []
        self._trade_share = []
        self._trade = None
        self._bill = None

    @property
    def account(self):
        return self._account

    @property
    def bundles(self):
        return self._bundles
    
    @property
    def indices(self):
        return self._indices
    
    @property
    def trade(self):
        return self._trade

    @property
    def amount_orders(self):
        return len(self._bundles)
    
    @property
    def trade_share(self):
        return self._trade_share
    
    @trade_share.setter
    def trade_share(self, value):
        self._trade_share = value

    def add_order(self, bundle, bid, indice):
        self._bundles.append(bundle)
        self._bids.append(bid)
        self._indices.append(indice)

    def get_concatenated_bundles(self):
        return np.array(self._bundles).T

    def get_concatenated_bids(self):
        return np.array(self._bids)
    
    def calculate_trade(self):
        self._trade = sum([bundle * trade_share for bundle, trade_share in zip(self._bundles, self._trade_share)])

    def calculate_bill(self, mkt_prices):
        self._bill = np.sum(np.multiply(self._trade, mkt_prices))
    
    def get_trade_information(self):
        trade = utils.prepare_for_sending(self._trade)
        bill = utils.prepare_for_sending(self._bill)

        return self._account, trade, bill

