import unittest

from lem_sim import utils


class UtilsTest(unittest.TestCase):

    def test_split_list_into_n_chunks(self):

        self.assertEqual(
            [[1, 2], [3, 4]],
            utils.split_list_into_n_chunks([1, 2, 3, 4], 2))
        self.assertEqual(
            [[5, 6], [7, 8]],
            utils.split_list_into_n_chunks([[5, 6], [7, 8]], 2))
        self.assertEqual(
            [[9, 10], [11, 12], [13, 14]],
            utils.split_list_into_n_chunks([[9, 10], [11, 12], [13, 14]], 3)
        )


if __name__ == '__main__':
    unittest.main()
