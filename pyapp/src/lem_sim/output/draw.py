import click as c


def print_central_problem(central_problem):
        c.secho('\nCentral LP ', bg='white', fg='black')
        central_problem.show()


def print_agents_lps(variables):
        c.secho('\n_______________________________')

        for index, agent in enumerate(variables.agent_pool):
                c.secho('\nLP of Agent {} '.format(index + 1), bg='green', fg='white')
                agent.optimization_problem.show()
                c.secho('\nBundle Attributes')
                c.secho('Improving Bundle: {}'.format(agent.bundle_set))
                c.secho('Bid: {}'.format(agent.bid))

        c.secho('_______________________________')
