import click as c
import numpy as np

from lem_sim import globalmemory as mem
from lem_sim import linearoptimization as lp
from lem_sim import output


@c.command()
@c.option('--connection', type=c.Choice(['docker', 'ip']), default='docker')
def main(connection):

    ''' initial setup of simulation '''
    var = mem.Variables(connection)
    lp.decompose(var)
    output.print_central_problem(var.central_problem)
    print(var.dealer)
    for agent in var.agent_pool:
        print(agent)

    var.dealer.set_mkt_prices()
    market_prices = var.dealer.mkt_prices
    equal_market_prices = False
    iteration = 1

    while(not equal_market_prices):
        ''' main simulation loop '''

        for agent in var.agent_pool:
            agent.get_mkt_prices()
            agent.determine_bundle_attributes()
            agent.set_order()

        var.dealer.get_orders()
        var.dealer.create_mmp()
        var.dealer.solve_mmp()
        var.dealer.set_trades()
        var.dealer.delete_order()
        var.dealer.calculate_resource_inventory()
        var.dealer.set_mkt_prices()

        for agent in var.agent_pool:
            agent.get_bill()
            agent.get_trade()
            agent.add_trade_to_shared_resources()

        output.print_iteration_stats(var, iteration)

        iteration += 1
        if(np.array_equal(market_prices, var.dealer.mkt_prices)):
            equal_market_prices = True
        else:
            market_prices = var.dealer.mkt_prices


if __name__ == '__main__':
    main()
