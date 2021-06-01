import unittest
from theory import ChinesePostmanEulerian as cp, Util
from theory import eulerian as euler

class MyTestCase(unittest.TestCase):
    def test_eulerian(self):
        edges =[(0, 1), (0, 3), (1, 2), (2, 3), (2, 4), (3, 4)]
        n = 5
        self.assertEqual(True, euler.is_eulerian_path(edges, cp.find_eulerian_path(edges, n)))

    def test_is_eulerian_false(self):
        edges = [(0, 1), (0, 3), (0, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)]
        n = 6
        self.assertEqual(False, euler.is_eulerian(Util.adj_list(edges, n, False)))

    def test_eulerian_path(self):
        edges = [(0,1), (0,2), (2,4), (1,3), (4,6), (3,5), (6,8), (5,7), (7,9), (8,9)]
        n = 10
        self.assertEqual(True, euler.is_eulerian_path(edges, cp.find_eulerian_path(edges, n)))


if __name__ == '__main__':
    unittest.main()
