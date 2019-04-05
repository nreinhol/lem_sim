from lem_sim import globalmemory as mem
from lem_sim import linearoptimization as lp
from lem_sim import output

import click


@click.command()
@click.option('--connection', type=click.Choice(['docker', 'ip']), default='docker')
def main(connection):

    variables = mem.Variables(connection)
    central_problem = lp.CentralProblem()
    lp.decompose(central_problem, variables)

    output.print_central_problem(central_problem)
    output.print_agents_lps(variables)


if __name__ == '__main__':
    main()
