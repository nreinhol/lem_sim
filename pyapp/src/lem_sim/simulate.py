import click
import numpy as np

from lem_sim import globalmemory as mem
from lem_sim import linearoptimization as lp
from lem_sim import output


@click.command()
@click.option('--connection', type=click.Choice(['docker', 'ip']), default='docker')
def main(connection):

    ''' initial setup of simulation '''
    var = mem.Variables(connection)
    lp.decompose(var)
    output.print_central_problem(var.central_problem)
    for agent in var.agent_pool:
        print(agent)
    print(var.dealer)

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

        for agent in var.agent_pool:
            agent.get_bill()
            agent.get_trade()
            agent.add_trade_to_shared_resources()

        var.dealer.delete_order()
        var.dealer.calculate_resource_inventory()
        var.dealer.set_mkt_prices()

        print('---------- Iteration {} ----------'.format(iteration))
        for agent in var.agent_pool:
            print(agent)
        print(var.dealer)

        iteration += 1
        if(np.array_equal(market_prices, var.dealer.mkt_prices)):
            equal_market_prices = True
        else:
            market_prices = var.dealer.mkt_prices


if __name__ == '__main__':
    main()
