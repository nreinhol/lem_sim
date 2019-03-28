from lem_sim import globalmemory as mem
from lem_sim import linearoptimization as lp

import click


@click.command()
@click.option('--connection', type=click.Choice(['docker', 'ip']))
def main(connection):
    variables = mem.Variables(connection)
    central_problem = lp.CentralProblem()
    lp.decompose(central_problem, variables)

    '''
    # get two specific agents out of list
    agent_one = variables.agent_pool[0]
    agent_two = variables.agent_pool[1]

    print('balance before tx: {}'.format(agent_two.balance))
    agent_one.send_transaction(agent_two.account_address, 1000000000000000000)
    print('balance after tx: {}'.format(agent_two.balance))
    '''


if __name__ == '__main__':
    main()
