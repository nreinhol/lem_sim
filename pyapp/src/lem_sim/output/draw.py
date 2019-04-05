import click as c


def print_central_problem(central_problem):
        c.secho('\n Central LP ', bg='white', fg='black')
        central_problem.show()


def print_agents_lps(variables, decompose=True):
        c.secho('\n_______________________________')

        if(decompose):
                c.secho('decompose and distribute to:\n', bold=True)

        for index, agent in enumerate(variables.agent_pool):
                c.secho('\n LP of Agent {} '.format(index + 1), bg='green', fg='white')
                agent.optimization_problem.show()

        c.secho('_______________________________')
