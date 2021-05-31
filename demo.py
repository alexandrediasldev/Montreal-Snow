import argparse
import real.plot_path as pl
import itertools
import copy
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
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

    #print(odd_node_pairs)
    #print('Number of pairs: {}'.format(len(odd_node_pairs)))

    #origin_point = long[0], lat[0]
    #dest_point = long[-1], lat[-1]

    #print(origin_point)
    #print(dest_point)

    #pl.plot_path(lat, long, origin_point, dest_point)


if __name__ == '__main__':
    main()
