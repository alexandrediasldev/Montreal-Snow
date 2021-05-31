import argparse
import real.plot_path as pl
import itertools
import copy
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd

import plotly.graph_objects as go

def parse_argument():

    ps = argparse.ArgumentParser(description="Big demo.")
    ps.add_argument("--city",
                    type=str,
                    help="Specify city to search.")
    ps.add_argument("--country",
                    type=str,
                    help="Specify country to search.")
    args = ps.parse_args()
    if args.city is not None:
        if args.country is None:
            country = "France"
        else:
            country = args.country
    return args.city,args.country
def get_shortest_paths_distances(graph, pairs, edge_weight_name):
    """Compute shortest distance between each pair of nodes in a graph.  Return a dictionary keyed on node pairs (tuples)."""
    distances = {}
    for pair in pairs:
        distances[pair] = nx.dijkstra_path_length(graph, pair[0], pair[1], weight=edge_weight_name)
    return distances
def create_complete_graph(pair_weights, flip_weights=True):
    """
    Create a completely connected graph using a list of vertex pairs and the shortest path distances between them
    Parameters:
        pair_weights: list[tuple] from the output of get_shortest_paths_distances
        flip_weights: Boolean. Should we negate the edge attribute in pair_weights?
    """
    g = nx.Graph()
    for k, v in pair_weights.items():
        wt_i = - v if flip_weights else v
        g.add_edge(k[0], k[1], attr_dict={'distance': v, 'weight': wt_i})
    return g
def add_augmenting_path_to_graph(graph, min_weight_pairs):
    """
    Add the min weight matching edges to the original graph
    Parameters:
        graph: NetworkX graph (original graph from trailmap)
        min_weight_pairs: list[tuples] of node pairs from min weight matching
    Returns:
        augmented NetworkX graph
    """

    # We need to make the augmented graph a MultiGraph so we can add parallel edges
    graph_aug = nx.MultiGraph(graph.copy())
    for pair in min_weight_pairs:
        graph_aug.add_edge(pair[0],
                           pair[1],
                           attr_dict={'distance': nx.dijkstra_path_length(graph, pair[0], pair[1]),
                                      'trail': 'augmented'}
                          )
    return graph_aug
def create_eulerian_circuit(graph_augmented, graph_original, starting_node=None):
    """Create the eulerian path using only edges from the original graph."""
    euler_circuit = []
    naive_circuit = list(nx.eulerian_circuit(graph_augmented, source=starting_node))

    for edge in naive_circuit:
        edge_data = graph_augmented.get_edge_data(edge[0], edge[1])
        print(edge_data)
        if "attr_dict" in edge_data[0] and  edge_data[0]['attr_dict']['trail'] != 'augmented':
            # If `edge` exists in original graph, grab the edge attributes and add to eulerian circuit.
            edge_att = graph_original[edge[0]][edge[1]]
            euler_circuit.append((edge[0], edge[1], edge_att))
        else:
            aug_path = nx.shortest_path(graph_original, edge[0], edge[1], weight='distance')
            aug_path_pairs = list(zip(aug_path[:-1], aug_path[1:]))

            print('Filling in edges for augmented edge: {}'.format(edge))
            print('Augmenting path: {}'.format(' => '.join(str(aug_path))))
            print('Augmenting path pairs: {}\n'.format(aug_path_pairs))

            # If `edge` does not exist in original graph, find the shortest path between its nodes and
            #  add the edge attributes for each link in the shortest path.
            for edge_aug in aug_path_pairs:
                edge_aug_att = graph_original[edge_aug[0]][edge_aug[1]]
                euler_circuit.append((edge_aug[0], edge_aug[1], edge_aug_att))

    return euler_circuit


def main():

    city,country = parse_argument()
    if(city is None or country is None):
        print("City or country not found")
        return 1

    G = ox.graph_from_place(city + ', ' + country, network_type='drive')
    G = ox.utils_graph.get_undirected(G)
    #print(G.nodes(data=True))

    #print(len(G.nodes))
    #route = nx.shortest_path(G, list(G.nodes)[0], list(G.nodes)[-1])

    #long = []
    #lat = []
    #for i in route:
    #    point = G.nodes[i]
    #    long.append(point['x'])
    #    lat.append(point['y'])

    # 1: Calculate list of nodes with odd degree
    nodes_odd_degree = [v for v, d in G.degree if d % 2 == 1]
    # 2.1: Compute all possible pairs of odd degree nodes.
    odd_node_pairs = list(itertools.combinations(nodes_odd_degree, 2))
    # 2.2: Compute the shortest path between each node pair calculated in 1.
    # Compute shortest paths.  Return a dictionary with node pairs keys and a single value equal to shortest path distance.
    odd_node_pairs_shortest_paths = get_shortest_paths_distances(G, odd_node_pairs, 'distance')

    # Preview with a bit of hack (there is no head/slice method for dictionaries).
    print(dict(list(odd_node_pairs_shortest_paths.items())[0:10]))

    # 2.3: Generate the complete graph
    g_odd_complete = create_complete_graph(odd_node_pairs_shortest_paths, flip_weights=True)

    # Counts
    print('Number of nodes: {}'.format(len(g_odd_complete.nodes())))
    print('Number of edges: {}'.format(len(g_odd_complete.edges())))
    # Plot the complete graph of odd-degree nodes
    plt.figure(figsize=(8, 6))
    pos_random = nx.random_layout(g_odd_complete)

    node_positions = {node[0]: (node[1]['x'], -node[1]['y']) for node in G.nodes(data=True)}
    print(node_positions)

    nx.draw_networkx_nodes(g_odd_complete, node_positions, node_size=20, node_color="red")
    nx.draw_networkx_edges(g_odd_complete, node_positions, alpha=0.1)
    plt.axis('off')
    plt.title('Complete Graph of Odd-degree Nodes')
    plt.show()
    # Step 2.4: Compute Minimum Weight Matching
    # Compute min weight matching.
    # Note: max_weight_matching uses the 'weight' attribute by default as the attribute to maximize.
    odd_matching_dupes = nx.algorithms.max_weight_matching(g_odd_complete, True)

    print('Number of edges in matching: {}'.format(len(odd_matching_dupes)))
    print(odd_matching_dupes)

    # Convert matching to list of deduped tuples
    odd_matching = list(pd.unique([tuple(sorted([k, v])) for k, v in odd_matching_dupes]))

    # Counts
    print('Number of edges in matching (deduped): {}'.format(len(odd_matching)))
    print(odd_matching)

    plt.figure(figsize=(8, 6))

    # Plot the complete graph of odd-degree nodes
    nx.draw(g_odd_complete, pos=node_positions, node_size=20, alpha=0.05)

    # Create a new graph to overlay on g_odd_complete with just the edges from the min weight matching
    g_odd_complete_min_edges = nx.Graph(odd_matching)
    nx.draw(g_odd_complete_min_edges, pos=node_positions, node_size=20, edge_color='blue', node_color='red')

    plt.title('Min Weight Matching on Complete Graph')
    plt.show()

    plt.figure(figsize=(8, 6))

    # Plot the original trail map graph
    nx.draw(G, pos=node_positions, node_size=20, alpha=0.1, node_color='black')

    # Plot graph to overlay with just the edges from the min weight matching
    nx.draw(g_odd_complete_min_edges, pos=node_positions, node_size=20, alpha=1, node_color='red', edge_color='blue')

    plt.title('Min Weight Matching on Orginal Graph')
    plt.show()

    # Create augmented graph: add the min weight matching edges to g
    g_aug = add_augmenting_path_to_graph(G, odd_matching)

    # Counts
    print('Number of edges in original graph: {}'.format(len(G.edges())))
    print('Number of edges in augmented graph: {}'.format(len(g_aug.edges())))
    print("Augmented")
    print(g_aug.edges())
    #3.0: Compute Eulerian Circuit
    s = g_aug.edges()
    print(s)

    for s1 in s:
        source_s = s1[0]
        break
    naive_euler_circuit = list(nx.eulerian_circuit(g_aug, source=source_s))
    print('Length of eulerian circuit: {}'.format(len(naive_euler_circuit)))

    # Create the Eulerian circuit
    euler_circuit = create_eulerian_circuit(g_aug, G, source_s)
    print('Length of Eulerian circuit: {}'.format(len(euler_circuit)))

    # Preview first 20 directions of CPP solution
    for i, edge in enumerate(euler_circuit[0:20]):
        print(i, edge)

    # Computing some stats
    for edge in euler_circuit:
        print(edge[2][0])
    total_mileage_of_circuit = sum([edge[2][0]['length'] for edge in euler_circuit])
    total_mileage_on_orig_trail_map = sum(nx.get_edge_attributes(G, 'distance').values())
    _vcn = pd.value_counts(pd.value_counts([(e[0]) for e in euler_circuit]), sort=False)
    node_visits = pd.DataFrame({'n_visits': _vcn.index, 'n_nodes': _vcn.values})
    _vce = pd.value_counts(
        pd.value_counts([sorted(e)[0] + sorted(e)[1] for e in nx.MultiDiGraph(euler_circuit).edges()]))
    edge_visits = pd.DataFrame({'n_visits': _vce.index, 'n_edges': _vce.values})

    # Printing stats
    print('Mileage of circuit: {0:.2f}'.format(total_mileage_of_circuit))
    print('Mileage on original trail map: {0:.2f}'.format(total_mileage_on_orig_trail_map))
    print('Mileage retracing edges: {0:.2f}'.format(total_mileage_of_circuit - total_mileage_on_orig_trail_map))
    if(total_mileage_on_orig_trail_map != 0):
        percent = ((1 - total_mileage_of_circuit / total_mileage_on_orig_trail_map) * - 100)
    else:
        percent = 0
    print('Percent of mileage retraced: {0:.2f}%\n'.format(percent))

    print('Number of edges in circuit: {}'.format(len(euler_circuit)))
    print('Number of edges in original graph: {}'.format(len(G.edges())))
    print('Number of nodes in original graph: {}\n'.format(len(G.nodes())))

    print('Number of edges traversed more than once: {}\n'.format(len(euler_circuit) - len(G.edges())))

    print('Number of times visiting each node:')
    print(node_visits.to_string(index=False))

    print('\nNumber of times visiting each edge:')
    print(edge_visits.to_string(index=False))
    #print(odd_node_pairs)
    #print('Number of pairs: {}'.format(len(odd_node_pairs)))

    #origin_point = long[0], lat[0]
    #dest_point = long[-1], lat[-1]

    #print(origin_point)
    #print(dest_point)

    #pl.plot_path(lat, long, origin_point, dest_point)


if __name__ == '__main__':
    main()
