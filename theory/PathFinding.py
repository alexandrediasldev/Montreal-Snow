from theory import Util


def single_source_distances(n, adj, src, dst):
    """
    :param n: the number of vertices
    :param adj: the adjacency matrix with weights
    :param src: the source vertex
    :param dst: the destination vertex
    :return: an array representing the path between src and dst
    implementation of the djikstra algorithm since we do not have
    negative weights
    """
    dist = [None] * n
    dist[src] = 0
    todo = [src]
    parent = [None] * n
    while todo:
        s = todo.pop(0)
        for d in range(n):
            weight = adj[s][d]
            if (weight != 0):
                if dist[d] is None or dist[d] > (dist[s] + weight):
                    dist[d] = dist[s] + weight
                    todo.append(d)
                    parent[d] = s
    res = []
    while dst != src:
        res.insert(0, dst)
        dst = parent[dst]
    res.insert(0, src)
    return res
