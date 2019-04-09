import unittest
import numpy as np


class DecomposeTest(unittest.TestCase):

    def test_concatenate_two_rows_of_arrays(self):
        first_row = np.array([-1, -2])
        second_row = np.array([0, 0])
        result = np.concatenate((first_row, second_row), axis=None)
        expected = np.array([-1, -2, 0, 0])

        self.assertTrue(np.array_equal(result, expected))

    def test_add_identity_matrix(self):
        # create identity matrix with n = array size
        random_array = np.array([1, 2])
        n = random_array.size
        identity_matrix = np.identity(n)

        # add identity matrix to a given array
        array = np.array([[1, 3], [1, 1]])
        merged_array = np.concatenate((array, identity_matrix), axis=1)
        expected = np.array([[1, 3, 1, 0], [1, 1, 0, 1]])

        self.assertTrue(np.array_equal(merged_array, expected))

    def test_create_array_with_zeros(self):
        zeros = np.zeros(2)
        expected = np.array([0, 0])

        self.assertTrue(np.array_equal(zeros, expected))


if __name__ == '__main__':
    unittest.main()
