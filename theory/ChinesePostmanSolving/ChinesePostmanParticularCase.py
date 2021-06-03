from theory import Util, PathFinding
from theory.ChinesePostmanSolving import ChinesePostmanEulerian


def eulerianise(n, edges):
    """
    :param n: the number of vertices
    :param edges: the graph's edges
    add new edges to make the graph eulerian
    the graph is undirected and only has two odd degree vertices
    :return the new eulerian path and its length
    """
    adj_list = Util.adj_list(edges, n, False)
    odd_vertices = Util.odd_vertices(adj_list)

    adj_mat = Util.adj_matrix(edges, n, False)

    path = PathFinding.single_source_distances(n, adj_mat, odd_vertices[0], odd_vertices[1])
    n += len(path)
    for i in range(len(path) - 1):
        src = path[i]
        dst = path[i + 1]
        s = (src, dst, adj_mat[src][dst])
        edges.append(s)
    path = ChinesePostmanEulerian.find_eulerian_path(edges, n)
    length = 0
    for i in range(len(path) - 1):
        src = path[i]
        dst = path[i + 1]
        length += adj_mat[src][dst]
    return (length, path)
