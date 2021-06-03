from theory.ChinesePostmanSolving import ChinesePostmanEulerian, ChinesePostmanParticularCase
from theory import Util, PathFinding
from theory import eulerian
import sys


def eulerianise(edges, n, matches, adj_mat):
    """
    :param edges:  the graph edges
    :param n: the number of vertices
    :param matches: the list of odd vertices between which we must add their shortest path to make the graph eulerian
    :param adj_mat: the graph adjacency matrix
    :return: a pair representing the solution path to the chinese postman problem and its total length
    """
    for (src, dst ) in matches:
        path = PathFinding.single_source_distances(n, adj_mat, src, dst)
        for i in range(len(path)-1):
            edges.append((path[i], path[i+1]))
    eulerian_path =  ChinesePostmanEulerian.find_eulerian_path(edges, n)
    length = 0
    for i in range(len(eulerian_path) - 1):
        src = eulerian_path[i]
        dst = eulerian_path[i + 1]
        length += adj_mat[src][dst]
    return (length, eulerian_path)

def matchings_gen(pairs, matchings, nb, done=[], final=[]):
    """
    :param pairs: all possible pairings between odd vertices
    :param matchings: the resulting list of list of all possible matchings
    :param nb: the number of pairs in a single matching
    :param done: vertices already stored in the current matching
    :param final: a possible list of pairing covering all vertices
    """
    if pairs[0][0][0] not in done:
        done.append(pairs[0][0][0])
        for i in pairs[0]:
            f = final[:]
            val = done[:]
            if i[1] not in val:
                f.append(i)
            else:
                continue

            if len(f) == nb:
                matchings.append(f)
                return
            else:
                val.append(i[1])
                matchings_gen(pairs[1:], matchings, nb, val, f)

    else:
        matchings_gen(pairs[1:], matchings, nb, done, final)


def solving(edges, n):
    """
    :param edges: graph's edges
    :param n: number of vertices
    :return: an  array representing the cycle solution to the problem
    """

    adj_mat = Util.adj_matrix(edges, n)
    odd_vertices = Util.extract_odd_vertices(adj_mat)
    if len(odd_vertices) == 0:
        return ChinesePostmanEulerian.find_eulerian_path(edges, n)
    if len(odd_vertices) == 2:
        return ChinesePostmanParticularCase.eulerianise(edges, n)

    paths = []
    for i in range(n):
        if i in odd_vertices:
            paths.append(PathFinding.multi_dest_distances(n, adj_mat, i))
        else:
            paths.append([])

    pairs = []
    for i in range(len(odd_vertices) - 1):
        pairs.append([])
        for j in range(i + 1, len(odd_vertices)):
            pairs[i].append([odd_vertices[i], odd_vertices[j]])

    # [ [AB, AC, AD] , [ BC, BD], [ CD]  ]

    matchings = []
    matchings_gen(pairs, matchings, (len(pairs) + 1) // 2)

    minimal_match = []
    minimum = sys.maxsize
    for matching in matchings:
        size = 0
        for (src, dst) in matching:
            size += paths[src][dst]
        if size < minimum:
            minimum = size
            minimal_match = matching

    return eulerianise(edges, n, minimal_match, adj_mat)