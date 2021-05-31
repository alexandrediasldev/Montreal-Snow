def degres(adj_mat):
    """
    Calculates the degrees of each vertex
    :param adj_mat: the graph represented by an adjacency list
    :return: an array containing the degree for each vertex
    """
    n = len(adj_mat)
    res = [0] * n

    for i in range(n):
        res[i] = len(adj_mat[i])

    return res

def is_eulerian(adjs):
    """
    Checks if the graph is eulerian

    :param adjs: adjacency list representing the graph
    :return: boolean indicating if the graph is eulerian
    """
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
 edges = the edgelist of the given graph
"""
def is_eulerian_path(edges, path):
    if len(path) != len(edges) + 1:
        return False

