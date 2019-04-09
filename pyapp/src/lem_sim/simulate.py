import click
import numpy as np

from lem_sim import globalmemory as mem
from lem_sim import linearoptimization as lp
from lem_sim import output

''' Definition of the Central Optimization Problem '''
TARGET_COEFS = np.array([-1, -2, -1, -3])  # cost vectors (d)
INDIVIDUAL_RESOURCES = np.array([4, 9])  # individual resources (n)
INDIVIDUAL_COEFS = np.array([[2, 1, 0, 0], [0, 0, 2, 3]])  # individual coefficients(N)
SHARED_RESOURCES = np.array([8, 5])  # shared resources (c)
SHARED_COEFS = np.array([[1, 3, 2, 1], [1, 1, 1, 1]])  # shared coefficients (C)


@click.command()
@click.option('--connection', type=click.Choice(['docker', 'ip']), default='docker')
def main(connection):

    variables = mem.Variables(connection)
    central_problem = lp.OptimizationProblem(TARGET_COEFS, INDIVIDUAL_RESOURCES, INDIVIDUAL_COEFS, SHARED_RESOURCES, SHARED_COEFS)
    lp.decompose(central_problem, variables)

    output.print_central_problem(central_problem)
    output.print_agents_lps(variables)


if __name__ == '__main__':
    main()
