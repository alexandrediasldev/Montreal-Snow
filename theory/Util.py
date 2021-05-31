""""
edges = graph's edges
n = graph's number of vertices
is_directed = is the graph is directed
return : the adjacency list of the graph
"""
from typing import List, Any, Union


def adj_list(edges, n, is_directed): #adj list made from an edge list with n nodes
    successor = [[] for a in range(n)]

    for (a, b) in edges:
        successor[a].append(b)
        if not is_directed:
            successor[b].append(a)

    return successor

"""
function used in eulerian path 
removes an edge from the list.
Tries both permutations for undirected graph

remaining_edges: list containing the remaining edges to operate on
vertex: the first vertex of the edge
dest: the last vertex of the edge
"""
def remove_edge(remaining_edges, vertex, dest, directed=False):

    if remaining_edges == None:
        return

    p1 = (vertex, dest)
    is_p1 = p1 in remaining_edges

    if is_p1:
        i = remaining_edges.index(p1)

    if not directed and not is_p1:
       p2 = (dest, vertex)

       if p2 in remaining_edges:
          i = remaining_edges.index(p2)
    else:
        return

    remaining_edges.pop(i)

def extract_odd_vertice(adj_mat):
    n = len(adj_mat)
    res = [0] * n

    for i in range(n):
        res[i] = len(adj_mat[i])

    return res

def odd_vertices(adj_list):
    res = []

    for d in adj_list:
        if len(d) % 2 == 1:
            res.append(d)

    return res

def pair_odd_vertices(odd_vertices, edges, n):
    """
        FIXME
    """
    return
