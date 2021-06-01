import unittest

from theory import PathFinding, Util


class MyTestCase(unittest.TestCase):
    def test_Dijkstra(self):
        edges = [(0, 1, 1), (0, 2, 1), (0, 3, 1), (1, 2, 1), (3, 4, 1), (4, 5, 1), (5, 6, 1), (4, 8, 1), (8, 7, 1), (6, 7, 1)]
        n = 9
        src = 0
        dst = 4
        self.assertEqual([0, 3, 4], PathFinding.single_source_distances(n, Util.adj_matrix(edges, 9, False), src, dst))

    def test_Dijkstra_complex(self):
        edges = [(0, 1, 1), (1, 2, 1), (0, 3, 1), (2, 5, 1), (3, 4, 3), (0, 7, 6), (5, 6, 1), (4, 8, 2), (8, 7, 1), (6, 7, 1)]
        n = 9
        src = 0
        dst = 7
        self.assertEqual([0, 1, 2, 5, 6, 7], PathFinding.single_source_distances(n, Util.adj_matrix(edges, 9, False), src, dst))

if __name__ == '__main__':
    unittest.main()
