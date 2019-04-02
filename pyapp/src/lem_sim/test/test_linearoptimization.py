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

    def test_remove_zero_rows_of_array(self):
        array = np.array([[2, 1], [0, 0], [1, 3], [1, 1]])
        array = lp.remove_zero_rows_of_array(array)

        self.assertTrue(np.array_equal(array, np.array([[2, 1], [1, 3], [1, 1]])))


if __name__ == '__main__':
    unittest.main()
