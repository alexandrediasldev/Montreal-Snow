import unittest
from theory import Util


class MyTestCase(unittest.TestCase):
    def test_something(self):
        g1 = [(9, 1), (9, 3), (8, 0), (4, 1), (1, 2), (2, 7), (2, 4), (5, 2), (7, 5), (5, 4), (4, 6), (6, 3), (3, 6),
              (0, 8)]
        n = 10

        self.assertEqual(Util.kosaraju(n, g1), [[9], [1, 4, 2, 5, 7], [6, 3], [0, 8]])


if __name__ == '__main__':
    unittest.main()
