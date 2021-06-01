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
import real.convert_utils as cu

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

def stats(G, euler_circuit):
    # Computing some stats

    total_length_of_circuit = sum([edge[2][0]['length'] for edge in euler_circuit])
    total_length_on_orig_map = sum(nx.get_edge_attributes(G, 'length').values())
    _vcn = pd.value_counts(pd.value_counts([(e[0]) for e in euler_circuit]), sort=False)
    node_visits = pd.DataFrame({'number of visits': _vcn.index, 'number of nodes': _vcn.values})
    _vce = pd.value_counts(
        pd.value_counts([sorted(e)[0] + sorted(e)[1] for e in nx.MultiDiGraph(euler_circuit).edges()]))
    edge_visits = pd.DataFrame({'number of visits': _vce.index, 'number of edges': _vce.values})
    edge_visits= edge_visits.sort_values(by='number of visits')

    pl.plot_visiting_edges(edge_visits)
    pl.plot_visiting_nodes(node_visits)



    # Printing stats
    print("=========STATS=========")
    print('Length of path: {0:.2f} m'.format(total_length_of_circuit))
    print('Length of the original map: {0:.2f} m'.format(total_length_on_orig_map))
    print('Length spent retracing edges: {0:.2f} m'.format(total_length_of_circuit - total_length_on_orig_map))
    if (total_length_on_orig_map != 0):
        percent = ((1 - total_length_of_circuit / total_length_on_orig_map) * - 100)
    else:
        percent = 0
    print('Percent of mileage retraced: {0:.2f}% \n'.format(percent))

    print('Number of edges in circuit: {}'.format(len(euler_circuit)))
    print('Number of edges in original graph: {}'.format(len(G.edges())))
    print('Number of nodes in original graph: {}\n'.format(len(G.nodes())))

    print('Number of edges traversed more than once: {}\n'.format(len(euler_circuit) - len(G.edges())))

    #print('Number of times visiting each node:')
    #print(node_visits.to_string(index=False))

    #print('\nNumber of times visiting each edge:')
    #print(edge_visits.to_string(index=False))


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

    node_positions = gu.get_node_position(G)

    pl.plot_complete_graph_odd_degre(g_odd_complete, G, node_positions)

    # Step 2.4: Compute Minimum Weight Matching
    # Compute min weight matching.
    # Note: max_weight_matching uses the 'weight' attribute by default as the attribute to maximize.
    odd_matching_dupes = nx.algorithms.max_weight_matching(g_odd_complete, True)


    # Convert matching to list of deduped tuples
    odd_matching = gu.remove_dupes_from_matching(odd_matching_dupes)


    g_odd_complete_min_edges = gu.get_nodes_odd_complete_min_edges(odd_matching)

    pl.plot_min_weight_matching_complete(g_odd_complete, g_odd_complete_min_edges, odd_matching, node_positions)

    pl.plot_min_weight_matching_original(G, g_odd_complete_min_edges, node_positions)

    # Create augmented graph: add the min weight matching edges to g
    g_aug = ga.add_augmenting_path_to_graph(G, odd_matching)


    # 3.0: Compute Eulerian Circuit
    s = g_aug.edges()
    source_s = gu.get_first_element_from_multi_edge_graphe(s)
    # Create the Eulerian circuit
    naive_eulerian = False
    if(naive_eulerian):
        naive_euler_circuit = list(nx.eulerian_circuit(g_aug, source=source_s))
        euler_circuit = naive_euler_circuit
    else:
        euler_circuit = ga.create_eulerian_circuit(g_aug, G, source_s)


    stats(G,euler_circuit)
    route = cu.euler_circuit_to_route(euler_circuit)

    long, lat = cu.route_to_long_lat(G, route)

    # print(odd_node_pairs)
    # print('Number of pairs: {}'.format(len(odd_node_pairs)))

    origin_point, dest_point = cu.long_lat_to_points(long, lat)

    pl.plot_path(lat, long, origin_point, dest_point)


if __name__ == '__main__':
    main()
