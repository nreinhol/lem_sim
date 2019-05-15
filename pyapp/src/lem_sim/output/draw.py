import click as c


def print_initial_setup(var):
        c.secho('\n__________________________________ ', fg='green', bold=True)
        c.secho('CENTRAL LP ', fg='green', bold=True)
        c.secho(var.central_problem.__str__())
        c.secho('\n__________________________________ ', fg='green', bold=True)
        c.secho('INITIAL SETUP', fg='green', bold=True)
        c.secho(var.dealer.__str__())

        for agent in var.agent_pool:
                c.secho(agent.__str__())


def print_iteration_stats(var, iteration):
        c.secho('\n__________________________________ ', fg='green', bold=True)
        c.secho('ITERATION {}'.format(iteration), fg='green', bold=True)
        c.secho(var.dealer.__str__())

        for agent in var.agent_pool:
                c.secho(agent.__str__())

def print_verify_strong_duality_failed(agent):
        c.secho('\n{} did not accept the trades bill!'.format(agent.name), fg='red', bold=True)
