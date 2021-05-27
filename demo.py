import argparse

import osmnx as ox


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

        city = ox.graph_from_place(args.city + ', ' + country, network_type='drive')

        for u, v, keys in city.edges(keys=True):
            print(u, v, keys)

        ax = ox.plot_graph(city)


if __name__ == '__main__':
    main()
