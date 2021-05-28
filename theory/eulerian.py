def degres(adj_mat):
    n = len(adj_mat)
    res = [0] * n

    for i in range(n):
        res[i] = len(adj_mat[i])

    return res
#adjs : adjacent_list
def is_eulerian(adjs): #check if adjs is eulerian
    odds = degres(adjs)
    ct = 0

    for v in odds:

        if v % 2 == 0:
            ct += 1

        if ct > 2:
            return False

    return ct == 0 or ct == 2


""""
used to test the eulerian path creation
 path = the path to test
 edges = 
"""
def is_eulerian_path(edges, path):
    if len(path) != len(edges) + 1:
        return False

