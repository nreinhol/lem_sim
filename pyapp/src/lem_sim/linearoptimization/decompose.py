import numpy as np


def decompose(central_problem, var):
        '''
        d = target coefs
        n = individual resources
        N = individual coefs
        c = shared resources
        C = shared coefs '''

        d, n, N, C = split_central_problem(central_problem, var.amount_agents)
        c = central_problem.shared_resources
        C = remove_zero_rows_of_individual_coefs(C)

        print(c.tolist())


def split_central_problem(central_problem, amount_agents):
        d = np.split(central_problem.target_coefs, amount_agents, axis=0)
        n = np.split(central_problem.individual_resources, amount_agents, axis=0)
        N = np.split(central_problem.individual_coefs, amount_agents, axis=1)
        C = np.split(central_problem.shared_coefs, amount_agents, axis=1)

        return d, n, N, C


def remove_zero_rows_of_individual_coefs(N):
        N_removed = []
        for N_j in N:
                N_removed.append(N_j[~np.all(N_j == 0, axis=1)])

        return N_removed
