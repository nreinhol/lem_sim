from lem_sim import linearoptimization as lp
from lem_sim import globalmemory as mem

import click


@click.command()
@click.option('--connection', type=click.Choice(['docker', 'port']))
def main(connection):
    variables = mem.Variables(connection)
    
    # create optimization problem
    target_coefs = [-1, -2, -1, -3]
    constraint_coefs = [[2, 0, 1, 1], [1, 0, 3, 1], [0, 2, 2, 1], [0, 3, 1, 1]]
    constraint_bounds = [4, 9, 8, 5]
    central_problem = lp.OptimizationProblem(target_coefs, constraint_coefs, constraint_bounds)

    # get two specific agents out of list
    agent_one = variables.agent_pool[0]
    agent_two = variables.agent_pool[1]

    print('balance before tx: {}'.format(agent_two.balance))
    agent_one.send_transaction(agent_two.account_address, 1000000000000000000)
    print('balance after tx: {}'.format(agent_two.balance))


if __name__ == '__main__':
    main()
