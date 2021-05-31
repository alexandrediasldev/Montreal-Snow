# Here we are simply finding an eulerian cycle
from theory import eulerian
from theory import Util

"""
procedure FindEulerPath(V)
  1. iterate through all the edges outgoing from vertex V;
       remove this edge from the graph,
       and call FindEulerPath from the second end of this edge;
  2. add vertex V to the answer.
"""

"""

adj = The adjacency List
vertex = the current vertex
remaining_edges = list of remaining edges to visit 
res = list of vertex , eulerian path

"""
def find_eulerian_path_auxiliary(adj, vertex, remaining_edges, res=[]):

    for dest in adj[vertex]:
        if (vertex, dest) in remaining_edges or (dest, vertex) in remaining_edges :
            Util.remove_edge(remaining_edges, vertex, dest)
            find_eulerian_path_auxiliary(adj, dest, remaining_edges, res)

    res.append(vertex)

def find_eulerian_path(edges, n):
    res = []
    vertex = 0
    remaining_edges = edges.copy()
    adj = Util.adj_list(edges, n, False)

    assert (eulerian.is_eulerian(adj))
    degres = eulerian.degres(adj)

    for i in range(len(degres)):
        if  degres[i]% 2 == 1:
            vertex = i
            break

    find_eulerian_path_auxiliary(adj, vertex, remaining_edges, res)
    return res

