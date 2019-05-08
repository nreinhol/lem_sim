import click

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

    ''' main simulation loop '''
    var.dealer.set_mkt_prices()

    for agent in var.agent_pool:
        agent.get_mkt_prices()
        agent.determine_bundle_attributes()
        agent.set_order()
    
    output.print_agents_lps(var)

    var.dealer.get_orders()
    var.dealer.create_mmp()
    var.dealer.solve_mmp()
    var.dealer.set_trades()

    for agent in var.agent_pool:
        agent.get_bill()
        agent.get_trade()
        agent.get_mkt_prices()
    
    var.dealer.delete_order()
    var.dealer.get_orders()



if __name__ == '__main__':
    main()

