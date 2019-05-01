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
    var.dealer.set_mkt_prices()  # dealer sets mktprices

    for agent in var.agent_pool:  # agents get mktprices and calc bundle
        agent.get_mkt_prices()
        agent.determine_bundle_attributes()

    output.print_agents_lps(var)


if __name__ == '__main__':
    main()
