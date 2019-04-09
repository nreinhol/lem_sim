import unittest
import numpy as np
from scipy.optimize import linprog

from lem_sim import linearoptimization as lp


class LinearOptimizationTest(unittest.TestCase):

    def test_solve_problem(self):
        target_coefs = np.array([1, -2, -1, -3])
        constraint_coefs = np.array([[2, 1, 0, 0], [0, 0, 2, 3], [1, 3, 2, 1], [1, 1, 1, 1]])
        constraint_bounds = np.array([4, 9, 8, 5])

        self.assertIsNotNone(linprog(target_coefs, A_ub=constraint_coefs, b_ub=constraint_bounds))

    def test_split_array_into_two(self):
        constraint_coefs = np.array([[2, 1, 0, 0], [0, 0, 2, 3], [1, 3, 2, 1], [1, 1, 1, 1]])
        splitted_constraint_coefs = np.split(constraint_coefs, 2, axis=1)
        array = np.array([[2, 1], [0, 0], [1, 3], [1, 1]])

        self.assertTrue(np.array_equal(splitted_constraint_coefs[0], array))

    def test_split_array_into_four(self):
        constraint_coefs = np.array([[2, 1, 0, 0], [0, 0, 2, 3], [1, 3, 2, 1], [1, 1, 1, 1]])
        splitted_constraint_coefs = np.split(constraint_coefs, 4, axis=1)
        array = np.array([[2], [0], [1], [1]])

        self.assertTrue(np.array_equal(splitted_constraint_coefs[0], array))

    def test_solve_bundle_determination(self):
        TARGET_COEFS = np.array([-1, -2])  # cost vectors (d)
        INDIVIDUAL_RESOURCES = np.array([4])  # individual resources (n)
        INDIVIDUAL_COEFS = np.array([[2, 1]])  # individual coefficients(N)
        SHARED_RESOURCES = np.array([4, 1])  # shared resources (c)
        SHARED_COEFS = np.array([[1, 3], [1, 1]])  # shared coefficients (C)

        optimization_problem = lp.OptimizationProblem(TARGET_COEFS, INDIVIDUAL_RESOURCES, INDIVIDUAL_COEFS, SHARED_RESOURCES, SHARED_COEFS)
        bundle_size = optimization_problem.shared_resources.size

        bundle_target_coefs = np.concatenate((optimization_problem.target_coefs, np.zeros(bundle_size)))
        bundle_individual_coefs = np.concatenate((optimization_problem.individual_coefs, np.zeros(optimization_problem.individual_coefs.shape)), axis=1)
        bundle_shared_coefs = np.concatenate((optimization_problem.shared_coefs, np.identity(optimization_problem.shared_resources.size, dtype=float) * (-1)), axis=1)

        bundle_coefs = np.concatenate((bundle_individual_coefs, bundle_shared_coefs))
        bundle_resources = np.concatenate((INDIVIDUAL_RESOURCES, SHARED_RESOURCES))

        result = linprog(bundle_target_coefs, bundle_coefs, bundle_resources)
        self.assertTrue(np.array_equal(result.x[-bundle_size:], np.array([8, 3])))


if __name__ == '__main__':
    unittest.main()
