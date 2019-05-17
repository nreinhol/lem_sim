from lem_sim import output


def initial_setup(var, draw=True):
    if(draw):
        output.print_initial_setup(var)

    output.log_initial_setup(var)


def iteration_stats(var, iteration, draw=True):
    if(draw):
        output.print_iteration_stats(var, iteration)

    output.log_iteration_stats(var, iteration)


def verify_strong_duality_failed(agent, draw=True):
    if(draw):
        output.print_verify_strong_duality_failed(agent)

    output.log_verify_strong_duality_failed(agent)
