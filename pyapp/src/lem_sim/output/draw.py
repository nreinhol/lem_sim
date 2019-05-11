import click as c


def print_central_problem(central_problem):
        c.secho('\n__________________________________ ', fg='green', bold=True)
        c.secho('\nCentral LP ', bg='white', fg='black')
        central_problem.show()
        c.secho('\n__________________________________ ', fg='green', bold=True)


def print_iteration_stats(var, iteration):
        c.secho('\n__________ Iteration {} __________ '.format(iteration), fg='green', bold=True)
        c.secho(var.dealer.__str__())

        for agent in var.agent_pool:
                c.secho(agent.__str__())
