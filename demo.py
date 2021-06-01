import argparse
import real.plot_path as pl
import itertools
import copy
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd
import real.graph_utils as gu
import real.graph_algo as ga

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
    return args.city, args.country


def euler_circuit_to_route(euler_circuit):
    route = []
    for edge in euler_circuit:
        route.append(edge[0])
    return route


def route_to_long_lat(G, route):
    long = []
    lat = []
    for i in route:
        point = G.nodes[i]
        long.append(point['x'])
        lat.append(point['y'])
    return long, lat


def long_lat_to_points(long, lat):
    origin_point = long[0], lat[0]
    dest_point = long[-1], lat[-1]
    return origin_point, dest_point


def main():
    city, country = parse_argument()
    if (city is None or country is None):
        print("City or country not found")
        return 1

    G = ox.graph_from_place(city + ', ' + country, network_type='drive')
    G = ox.utils_graph.get_undirected(G)

    # 1: Calculate list of nodes with odd degree
    nodes_odd_degree = gu.get_nodes_odd_degree(G)
    # 2.1: Compute all possible pairs of odd degree nodes.
    odd_node_pairs = gu.compute_pairs_of_odd_degree_nodes(nodes_odd_degree)
    # 2.2: Compute the shortest path between each node pair calculated in 1.
    # Compute shortest paths.  Return a dictionary with node pairs keys and a single value equal to shortest path distance.
    odd_node_pairs_shortest_paths = ga.get_shortest_paths_distances(G, odd_node_pairs, 'distance')

    # Preview with a bit of hack (there is no head/slice method for dictionaries).
    # print(dict(list(odd_node_pairs_shortest_paths.items())[0:10]))

    # 2.3: Generate the complete graph
    g_odd_complete = ga.create_complete_graph(odd_node_pairs_shortest_paths, flip_weights=True)

    # Counts
    print('Number of nodes: {}'.format(len(g_odd_complete.nodes())))
    print('Number of edges: {}'.format(len(g_odd_complete.edges())))
    node_positions = gu.get_node_position(G)

    pl.plot_complete_graph_odd_degre(g_odd_complete, G, node_positions)

    # Step 2.4: Compute Minimum Weight Matching
    # Compute min weight matching.
    # Note: max_weight_matching uses the 'weight' attribute by default as the attribute to maximize.
    odd_matching_dupes = nx.algorithms.max_weight_matching(g_odd_complete, True)

    print('Number of edges in matching: {}'.format(len(odd_matching_dupes)))
    print(odd_matching_dupes)

    # Convert matching to list of deduped tuples
    odd_matching = gu.remove_dupes_from_matching(odd_matching_dupes)

    # Counts
    print('Number of edges in matching (deduped): {}'.format(len(odd_matching)))
    print(odd_matching)
    g_odd_complete_min_edges = gu.get_nodes_odd_complete_min_edges(odd_matching)

    pl.plot_min_weight_matching_complete(g_odd_complete, g_odd_complete_min_edges, odd_matching, node_positions)

    pl.plot_min_weight_matching_original(G, g_odd_complete_min_edges, node_positions)

    # Create augmented graph: add the min weight matching edges to g
    g_aug = ga.add_augmenting_path_to_graph(G, odd_matching)

    # Counts
    print('Number of edges in original graph: {}'.format(len(G.edges())))
    print('Number of edges in augmented graph: {}'.format(len(g_aug.edges())))
    print("Augmented")
    print(g_aug.edges())
    # 3.0: Compute Eulerian Circuit
    s = g_aug.edges()
    source_s = gu.get_first_element_from_multi_edge_graphe(s)
    naive_euler_circuit = list(nx.eulerian_circuit(g_aug, source=source_s))
    print('Length of eulerian circuit: {}'.format(len(naive_euler_circuit)))

    # Create the Eulerian circuit
    euler_circuit = ga.create_eulerian_circuit(g_aug, G, source_s)
    print('Length of Eulerian circuit: {}'.format(len(euler_circuit)))

    # Preview first 20 directions of CPP solution
    for i, edge in enumerate(euler_circuit[0:20]):
        print(i, edge)

    # Computing some stats

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
    if (total_mileage_on_orig_trail_map != 0):
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
    route = euler_circuit_to_route(euler_circuit)

    long, lat = route_to_long_lat(G, route)

    # print(odd_node_pairs)
    # print('Number of pairs: {}'.format(len(odd_node_pairs)))

    origin_point, dest_point = long_lat_to_points(long, lat)

    pl.plot_path(lat, long, origin_point, dest_point)


if __name__ == '__main__':
    main()
