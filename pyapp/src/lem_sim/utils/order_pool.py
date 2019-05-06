import numpy as np

from lem_sim import utils


class OrderPool(object):

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
