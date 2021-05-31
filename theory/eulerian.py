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

        if v % 2 == 1:
            ct += 1

        if ct > 2:
            return False

    return ct == 0 or ct == 2

def is_eulerian_cycle(edges, cycle):

    """
    checks if the given cycle is eulerian

    :param edges: edge list representing the graph
    :param path: the cycle to test
    :return: True if the cyclee is eulerian, False otherwise
    """

    if len(cycle) != len(edges):
        return False

    visited = [False] * len(edges)

    for i in range(len(cycle)):

        if i == len(cycle) - 1:
            Va, Vb = cycle[i], cycle[0]
        else:
            Va, Vb = cycle[i], cycle[i + 1]

        tuple_1 = (Va, Vb)
        tuple_2 = (Vb, Va)

        for j in range(len(edges)):
            if tuple_1 == edges[j] or tuple_2 == edges[j]:
                visited[j] = True

    for b in visited:
        if not b:
            return False

    return True

def generate_eulerian_cycle(edges):


def is_eulerian_path(edges, path):
    """
    used to test the eulerian path creation

    :param edges: the edgelist representing the graph
    :param path: the path to test
    :return: True if it is eulerian False otherwise
    """

    if len(path) - 1 != len(edges):
        return False

    visited = [False] * len(edges)

    for i in range(len(path)) - 1:

        Va, Vb = path[i], path[i + 1]
        tuple_1 = (Va, Vb)
        tuple_2 = (Vb, Va)

        for j in range(len(edges)):
            if tuple_1 == edges[j] or tuple_2 == edges[j]:
                visited[j] = True

    for b in visited:
        if not b:
            return False

    return True

