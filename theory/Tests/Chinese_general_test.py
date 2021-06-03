import unittest

from theory import eulerian
from theory.ChinesePostmanSolving import ChinesePostmanGeneralCase


class MyTestCase(unittest.TestCase):
    def test_something(self):
        edges = [(0,1,1),(0,3,2),(1,2,3),(1,3,5),(3,4,4),(2,4,6),(2,5,2),(4,5,1)]
        n = 6
        r = ChinesePostmanGeneralCase.solving(edges, n)
        self.assertEqual(30, r[0])
        self.assertEqual(True, eulerian.is_eulerian_path(edges, r[1]))


if __name__ == '__main__':
    unittest.main()
