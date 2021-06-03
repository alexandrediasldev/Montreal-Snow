import unittest

from theory.ChinesePostmanSolving import ChinesePostmanParticularCase
from theory import eulerian


class MyTestCase(unittest.TestCase):
    def test_Chinese_basic_particular(self):
        edges = [(0,1,70),(0,5,70),(1,5,50),(1,2,50),(1,4,50),(2,4,50),(2,3,50),(3,4,70),(4,5,60),(3,6,70),(3,7,120),(6,7,70), (5,7,60)]
        n = 8
        res = ChinesePostmanParticularCase.eulerianise(n, edges)
        self.assertEqual(1000, res[0])
        self.assertEqual(True, eulerian.is_eulerian_path(edges, res[1]))

if __name__ == '__main__':
    unittest.main()
