import itertools
import pandas as pd
import networkx as nx

def get_nodes_odd_degree(G):
    nodes_odd_degree = [v for v, d in G.degree if d % 2 == 1]
    return nodes_odd_degree


def get_node_position(G):
    return {node[0]: (node[1]['x'], -node[1]['y']) for node in G.nodes(data=True)}


def compute_pairs_of_odd_degree_nodes(G):
    odd_node_pairs = list(itertools.combinations(G, 2))
    return odd_node_pairs

def get_nodes_odd_complete_min_edges(odd_matching):
    return nx.Graph(odd_matching)

def remove_dupes_from_matching(odd_matching_dupes):
    return list(pd.unique([tuple(sorted([k, v])) for k, v in odd_matching_dupes]))

def get_first_element_from_multi_edge_graphe(multi_edge_graph):
    for e in multi_edge_graph:
        return e[0]