# Here we are simply finding an eulerian cycle
from theory import eulerian
from theory import Util


def is_bridge(adj, start, dst):
    """
    :param adj: graph's adjacency list
    :param start: the starting vertex
    :param dst: the destination vertex
    :return: true if start <-> dst is a bridge
    meaning going through this edge would ruin the eulerian path
    """
    if len(adj[start]) == 1:
        Util.remove_edge(adj, start, dst)
        return False

    count_1 = Util.reachable(adj, start, [False] * len(adj))
    Util.remove_edge(adj, start, dst)

    if count_1 == Util.reachable( adj, start, [False] * len(adj)) :
        return False
    adj[start].append(dst)
    adj[dst].append(start)
    return True



def path_aux(adj, start, res):
    """
    recursive function to find an eulerian path
    :param res the resulting path
    """
    for dst in adj[start]:
        if not is_bridge(adj, start, dst):
            res.append(dst)
            path_aux(adj, dst, res)


def find_eulerian_path(edges, n):
    """
    :param edges: list of the graph's edges
    :param n: the number of vertices
    :return: an array with the vertices to go through in order to have an eulerian path/cycle

    the graph is undirected
    """
    start = 0
    adj = Util.adj_list(edges, n, False)

    assert (eulerian.is_eulerian(adj))
    degrees = eulerian.degres(adj)

    for i in range(len(degrees)):
        if degrees[i] % 2 == 1:
            start = i
            break

    res = [start]
    path_aux(adj, start, res)

    return res
