def adj_list(edges, n, is_directed):
    """"
    edges = graph's edges
    n = graph's number of vertices
    is_directed = is the graph is directed
    return : the adjacency list of the graph
    """
    successor = [[] for _ in range(n)]

    for edge in edges:
        successor[edge[0]].append(edge[1])
        if not is_directed:
            successor[edge[1]].append(edge[0])

    return successor


def adj_matrix(edges, n, is_directed=False):
    """
    same as above bot returns adjacency matrix
    """
    matrix = [[0 for _ in range(n)] for _ in range(n)]

    for (src, dst, w) in edges:
        matrix[src][dst] = w
        if not is_directed:
            matrix[dst][src] = w

    return matrix


"""
function used in eulerian path 
removes an edge from the list.
Tries both permutations for undirected graph

remaining_edges: list containing the remaining edges to operate on
vertex: the first vertex of the edge
dest: the last vertex of the edge
"""


def remove_edge(adj, vertex, dest, is_directed=False):
    try:
        index = adj[vertex].index(dest)
        adj[vertex].pop(index)
    except ValueError:
        index = adj[dest].index(vertex)
        adj[dest].pop(index)
    if not is_directed:
        index = adj[dest].index(vertex)
        adj[dest].pop(index)


def extract_odd_vertices(adj_mat):
    """
    :param adj_mat: the graph adj matrix
    :return: a list of all the odd degree vertices
    """

    res = []
    n = len(adj_mat)
    for i in range(n):
        if (n - adj_mat[i].count(0)) % 2 == 1:
            res.append(i)

    return res


def odd_vertices(adj_list):
    """
    :param adj_list: the graph adj list
    :return: a list of all the odd degree vertices
    """
    res = []
    for i in range(len(adj_list)):
        if len(adj_list[i]) % 2 == 1:
            res.append(i)
    return res


def reachable(adj, vertex, visited):
    """
    :param adj: the graph adjacency list
    :param vertex: the current vertex
    :param visited: the list of visited vertices
    :return: the number of vertices connected to vertex

    This algorithm is based on a DFS an will be useful to find if we did not remove
    an important edge when finding an eulerian path
    """

    res = 1
    visited[vertex] = True
    for dst in adj[vertex]:
        if not visited[dst]:
            res += reachable(adj, dst, visited)
    return res
