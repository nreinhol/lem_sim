from lem_sim import output


def initial_setup(var):
    output.print_initial_setup(var)
    output.log_initial_setup(var)


def iteration_stats(var, iteration):
    output.print_iteration_stats(var, iteration)
    output.log_iteration_stats(var, iteration)
