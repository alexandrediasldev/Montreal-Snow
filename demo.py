import argparse
import real.plot_path as pl
import itertools
import copy
import networkx as nx
import osmnx as ox
import plotly.graph_objects as go


def main():
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

        G = ox.graph_from_place(args.city + ', ' + country, network_type='drive')
        G = ox.utils_graph.get_undirected(G)

        print(len(G.nodes))
        route = nx.shortest_path(G, list(G.nodes)[0], list(G.nodes)[-1])

        long = []
        lat = []
        for i in route:
            point = G.nodes[i]
            long.append(point['x'])
            lat.append(point['y'])
        nodes_odd_degree = [v for v, d in G.degree if d % 2 == 1]
        odd_node_pairs = list(itertools.combinations(nodes_odd_degree, 2))

        print(odd_node_pairs)
        print('Number of pairs: {}'.format(len(odd_node_pairs)))

        origin_point = long[0], lat[0]
        dest_point = long[-1], lat[-1]

        print(origin_point)
        print(dest_point)

        #pl.plot_path(lat, long, origin_point, dest_point)


if __name__ == '__main__':
    main()
