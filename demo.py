import argparse
import real.plot_path as pl
import networkx as nx
import osmnx as ox
import real.graph_utils as gu
import real.graph_algo as ga
import real.convert_utils as cu
import real.stats as st



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



def main():
    city, country = "Hampstead", "Canada"
    #if (city is None or country is None):
    #    print("Please specify --city and --country")
    #    print("Example: --city Kremlin-Bicetre --country France")
    #    return 1
    print("Specified city: ",city)
    print("Specified country: ",country)

    print("Getting map data from Osmnx")
    # Get the graph data from osmnx
    G = ox.graph_from_place(city + ', ' + country, network_type='drive')

    # Convert the graph to undirected
    G = ox.utils_graph.get_undirected(G)

    # Steps to solve the chinese postman problem:
    # 1: Calculate list of nodes with odd degree
    # 2: Add edges to the graph such that all nodes of odd degree are made even.
    # These added edges must be duplicates from the original graph
    #    2.1: Compute all possible pairs of odd degree nodes.
    #    2.2: Compute the shortest path between each node pair calculated in 1.
    #    2.3: Generate the complete graph
    #    2.4: Compute Minimum Weight Matching
    # 3.0: Compute Eulerian Circuit


    # Step 1: Calculate list of nodes with odd degree
    print("Step 1: Calculate list of nodes with odd degree")
    nodes_odd_degree = gu.get_nodes_odd_degree(G)
    # Step 2.1: Compute all possible pairs of odd degree nodes.
    print("Step 2.1: Compute all possible pairs of odd degree nodes.")
    odd_node_pairs = gu.compute_pairs_of_odd_degree_nodes(nodes_odd_degree)
    # Step 2.2: Compute the shortest path between each node pair calculated in 1.
    print("Step 2.2: Compute the shortest path between each node pair calculated in 1.")
    odd_node_pairs_shortest_paths = ga.get_shortest_paths_distances(G, odd_node_pairs, 'distance')

    # Step 2.3: Generate the complete graph
    print("Step 2.3: Generate the complete graph")
    g_odd_complete = ga.create_complete_graph(odd_node_pairs_shortest_paths, flip_weights=True)

    node_positions = gu.get_node_position(G)

    pl.plot_complete_graph_odd_degree(g_odd_complete, node_positions)

    # Step 2.4: Compute Minimum Weight Matching
    # Compute min weight matching.
    # Note: max_weight_matching uses the 'weight' attribute by default as the attribute to maximize.
    print("Step 2.4: Compute Minimum Weight Matching")
    odd_matching_dupes = nx.algorithms.max_weight_matching(g_odd_complete, True)

    # Convert matching to list of deduped tuples
    odd_matching = gu.remove_dupes_from_matching(odd_matching_dupes)


    # Create augmented graph: add the min weight matching edges to g
    g_aug = ga.add_augmenting_path_to_graph(G, odd_matching)

    # Step 3.0: Compute Eulerian Circuit
    print("Step 3.0: Compute Eulerian Circuit")
    s = g_aug.edges()
    source_s = gu.get_first_element_from_multi_edge_graphe(s)

    # Create the Eulerian circuit

    # Naive eulerian circuit from osmnx, that gives buggy results
    naive_eulerian = False
    if (naive_eulerian):
        naive_euler_circuit = list(nx.eulerian_circuit(g_aug, source=source_s))
        euler_circuit = naive_euler_circuit
    else:
        euler_circuit = ga.create_eulerian_circuit(g_aug, G, source_s)

    st.stats(G, euler_circuit)

    # Plot the minimum matchings
    g_odd_complete_min_edges = gu.get_nodes_odd_complete_min_edges(odd_matching)
    pl.plot_min_weight_matching_complete(g_odd_complete, g_odd_complete_min_edges, node_positions)
    pl.plot_min_weight_matching_original(G, g_odd_complete_min_edges, node_positions)

    # Convert the euleur circuit to a route
    route = cu.euler_circuit_to_route(euler_circuit)
    long, lat = cu.route_to_long_lat(G, route)
    origin_point, dest_point = cu.long_lat_to_points(long, lat)
    print("Plotting the route")
    # Plot the route
    pl.plot_path(lat, long, origin_point, dest_point)






if __name__ == '__main__':
    main()
