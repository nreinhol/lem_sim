import click as c
import numpy as np

from lem_sim import globalmemory as mem
from lem_sim import linearoptimization as lp
from lem_sim import output


@c.command()
@c.option('--connection', type=c.Choice(['docker', 'ip']), default='docker')
def main(connection):

    # initial setup of simulation
    var = mem.Variables(connection)
    lp.decompose(var)

    var.dealer.set_mkt_prices()
    market_prices = var.dealer.mkt_prices

    equal_market_prices = False
    iteration = 1

    output.initial_setup(var)

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
        var.dealer.calculate_resource_inventory()
        var.dealer.set_mmp_attributes()  # transact

        for agent in var.agent_pool:
            agent.get_bill()  # call
            agent.get_trade()  # transact
            agent.add_trade_to_shared_resources()

        output.iteration_stats(var, iteration)
        iteration += 1

        if(np.array_equal(market_prices, var.dealer.mkt_prices)):
            equal_market_prices = True
        else:
            market_prices = var.dealer.mkt_prices


if __name__ == '__main__':
    main()
