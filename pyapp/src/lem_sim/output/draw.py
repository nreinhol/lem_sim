import click as c


def print_initial_setup(var):
        c.secho('\n__________________________________ ', fg='green', bold=True)
        c.secho('CENTRAL LP ', fg='green', bold=True)
        var.central_problem.show()
        c.secho('\n__________________________________ ', fg='green', bold=True)
        c.secho('INITIAL SETUP', fg='green', bold=True)
        c.secho(var.dealer.__str__())

        for agent in var.agent_pool:
                c.secho(agent.__str__())


def print_iteration_stats(var, iteration):
        c.secho('\n__________ Iteration {} __________ '.format(iteration), fg='green', bold=True)
        c.secho(var.dealer.__str__())

        for agent in var.agent_pool:
                c.secho(agent.__str__())
