import numpy as np

from lem_sim import linearoptimization as lp


def decompose(central_problem, var):
        '''
        d = target coefs
        n = individual resources
        N = individual coefs
        c = shared resources
        C = shared coefs '''

        d, n, N, c, C = split_central_problem(central_problem, var.amount_agents)
        N = remove_zero_rows_of_individual_coefs(N)

        for d_j, n_j, N_j, c_j, C_j, agent_j in zip(d, n, N, c, C, var.agent_pool):
                optimization_problem_j = lp.OptimizationProblem(d_j, n_j, N_j, c_j, C_j)
                agent_j.optimization_problem = optimization_problem_j


def split_central_problem(central_problem, amount_agents):
        d = np.split(central_problem.target_coefs, amount_agents, axis=0)
        n = np.split(central_problem.individual_resources, amount_agents, axis=0)
        N = np.split(central_problem.individual_coefs, amount_agents, axis=1)
        c = distribute_shared_resources(central_problem.shared_resources, amount_agents)
        C = np.split(central_problem.shared_coefs, amount_agents, axis=1)

        return d, n, N, c, C


def remove_zero_rows_of_individual_coefs(N):
        return [N_j[~np.all(N_j == 0, axis=1)] for N_j in N]


def distribute_shared_resources(c, amount_agents):
        ''' distribute the shared resources into equally sized parts '''
        return [np.divide(c, amount_agents + 1) for i in range(amount_agents)]


def build_constraint_coefs_for_agents(N, C):
        return [np.concatenate((N_j, C_j)) for N_j, C_j in zip(N, C)]


def build_constraint_bounds_for_agents(n, c):
        return [np.concatenate((n_j, c_j)) for n_j, c_j in zip(n, c)]
