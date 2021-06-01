import osmnx as ox
import networkx as nx
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt


def plot_path(lat, long, origin_point, destination_point):
    """
    Given a list of latitudes and longitudes, origin
    and destination point, plots a path on a map

    Parameters
    ----------
    lat, long: list of latitudes and longitudes
    origin_point, destination_point: co-ordinates of origin
    and destination
    Returns
    -------
    Nothing. Only shows the map.
    """
    # adding the lines joining the nodes
    fig = go.Figure(go.Scattermapbox(
        name="Path",
        mode="lines",
        lon=long,
        lat=lat,
        marker={'size': 10},
        line=dict(width=4.5, color='blue')))

    # adding source marker
    fig.add_trace(go.Scattermapbox(
        name="Source",
        mode="markers",
        lon=[origin_point[1]],
        lat=[origin_point[0]],
        marker={'size': 12, 'color': "red"}))

    # adding destination marker
    fig.add_trace(go.Scattermapbox(
        name="Destination",
        mode="markers",
        lon=[destination_point[1]],
        lat=[destination_point[0]],
        marker={'size': 12, 'color': 'green'}))

    # getting center for plots:
    lat_center = np.mean(lat)
    long_center = np.mean(long)
    # defining the layout using mapbox_style
    fig.update_layout(mapbox_style="stamen-terrain",
                      mapbox_center_lat=30, mapbox_center_lon=-80)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox={
                          'center': {'lat': lat_center,
                                     'lon': long_center},
                          'zoom': 13})
    fig.show()


def plot_complete_graph_odd_degre(g_odd_complete, G, node_positions):
    plt.figure(figsize=(8, 6))
    pos_random = nx.random_layout(g_odd_complete)

    nx.draw_networkx_nodes(g_odd_complete, node_positions, node_size=20, node_color="red")
    nx.draw_networkx_edges(g_odd_complete, node_positions, alpha=0.1)
    plt.axis('off')
    plt.title('Complete Graph of Odd-degree Nodes')
    plt.show()


def plot_min_weight_matching_complete(g_odd_complete, g_odd_complete_min_edges, odd_matching, node_positions):
    plt.figure(figsize=(8, 6))

    # Plot the complete graph of odd-degree nodes
    nx.draw(g_odd_complete, pos=node_positions, node_size=20, alpha=0.05)

    # Create a new graph to overlay on g_odd_complete with just the edges from the min weight matching
    nx.draw(g_odd_complete_min_edges, pos=node_positions, node_size=20, edge_color='blue', node_color='red')

    plt.title('Min Weight Matching on Complete Graph')
    plt.show()


def plot_min_weight_matching_original(G, g_odd_complete_min_edges, node_positions):
    plt.figure(figsize=(8, 6))

    # Plot the original trail map graph
    nx.draw(G, pos=node_positions, node_size=20, alpha=0.1, node_color='black')

    # Plot graph to overlay with just the edges from the min weight matching
    nx.draw(g_odd_complete_min_edges, pos=node_positions, node_size=20, alpha=1, node_color='red', edge_color='blue')

    plt.title('Min Weight Matching on Orginal Graph')
    plt.show()


def plot_visiting_edges(edge_visits):
    edge_visits.plot.bar(x='n_visits', y='n_edges', rot=0)
    plt.show()


def plot_visiting_nodes(node_visits):
    node_visits.plot.bar(x='n_visits', y='n_nodes', rot=0)
    plt.show()
