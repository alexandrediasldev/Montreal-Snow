import unittest
from theory import ChinesePostmanEulerian as cp
from theory import eulerian as euler

class MyTestCase(unittest.TestCase):
    def test_eulerian(self):
        edges =[(0, 1), (0, 3), (1, 2), (2, 3), (2, 4), (3, 4)]
        n = 5
        self.assertEqual(True, euler.is_eulerian_path(edges, cp.find_eulerian_path(edges, n)))


if __name__ == '__main__':
    unittest.main()
