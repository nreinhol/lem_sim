import numpy as np

from lem_sim import globalmemory as mem
from lem_sim import linearoptimization as lp
from lem_sim import output


def main():

    # general setup of simulation
    var = mem.Variables()
    lp.decompose(var)

    # set initial inventory and market prices
    var.dealer.set_resource_inventory()
    var.dealer.set_mkt_prices()

    # set initial simulation parameter
    market_prices = var.dealer.mkt_prices
    equal_market_prices = False
    iteration = 1

    output.initial_setup(var, draw=True)

    # main simulation loop
    while(not equal_market_prices):

        for agent in var.agent_pool:
            agent.get_mkt_prices()  # call
            agent.determine_bundle_attributes()
            agent.set_order()  # transact

        var.dealer.get_orders()  # call
        var.dealer.create_mmp()
        var.dealer.solve_mmp()
        var.dealer.set_trades()  # transact
        var.dealer.delete_order()  # transact
        var.dealer.set_mkt_prices()  # transact
        var.dealer.set_mmp_attributes()  # transact

        for agent in var.agent_pool:
            agent.verify_strong_duality()  # call
            agent.accept_trade()  # transact
            agent.add_trade_to_shared_resources()

        var.dealer.recalculate_resource_inventory() # transact

        output.iteration_stats(var, iteration, draw=True)
        iteration += 1

        if(np.array_equal(market_prices, var.dealer.mkt_prices)):
            equal_market_prices = True
        else:
            market_prices = var.dealer.mkt_prices


if __name__ == '__main__':
    main()
