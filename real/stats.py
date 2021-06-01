import matplotlib.pyplot as plt
import pandas as pd
import real.plot_path as pl
import networkx as nx
import osmnx as ox

def stats(G, euler_circuit):
    """
    Compute stats about the graph, show them and plot them
    :param G: original graph
    :param euler_circuit: euler circuit
    """
    # Computing some stats

    total_length_of_circuit = sum([edge[2][0]['length'] for edge in euler_circuit])
    total_length_on_orig_map = sum(nx.get_edge_attributes(G, 'length').values())
    _vcn = pd.value_counts(pd.value_counts([(e[0]) for e in euler_circuit]), sort=False)
    node_visits = pd.DataFrame({'number of visits': _vcn.index, 'number of nodes': _vcn.values})
    _vce = pd.value_counts(
        pd.value_counts([sorted(e)[0] + sorted(e)[1] for e in nx.MultiDiGraph(euler_circuit).edges()]))
    edge_visits = pd.DataFrame({'number of visits': _vce.index, 'number of edges': _vce.values})
    edge_visits = edge_visits.sort_values(by='number of visits')



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

    #Plotting stats

    pl.plot_visiting_edges(edge_visits)
    pl.plot_visiting_nodes(node_visits)
    print("=======================")