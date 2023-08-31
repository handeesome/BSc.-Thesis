from pymnet import *
import pandas as pd
import closeness_centrality as cc
import numpy as np



def produce_centralities(net, layer, threshold):
    nx_net = nx.autowrap(net)
    deg_centrality = nx.degree_centrality(nx_net)
    degree_centrality_df = pd.DataFrame.from_dict(deg_centrality, orient='index', columns=['degree_centrality'])
    degree_centrality_df.index.name = 'node'
    degree_centrality_df.to_csv(f'docs/{layer}_degree_centrality_{threshold}.csv')
    print(f"degree centrality for layer {layer} is done!")

    # btwns_centrality = nx.betweenness_centrality(nx_net, k=int(len(deg_centrality)*0.01))
    btwns_centrality = nx.betweenness_centrality(nx_net, k=100)
    betweenness_centrality_df = pd.DataFrame.from_dict(
        btwns_centrality, orient='index', columns=['betweenness_centrality'])
    betweenness_centrality_df.index.name = 'node'
    betweenness_centrality_df.to_csv(f'docs/{layer}_betweenness_centrality_{threshold}.csv')
    print(f"betweenness centrality for layer {layer} is done!")
    
    clsns_centrality = cc.closeness_centrality(nx_net)
    clsns_centrality_df = pd.DataFrame.from_dict(clsns_centrality, orient='index', columns=['closeness_centrality'])
    clsns_centrality_df.index.name = 'node'
    clsns_centrality_df.to_csv(f'docs/{layer}_closeness_centrality_{threshold}.csv')
    print(f"closeness centrality for layer {layer} is done!")

    clustering_coefficient = nx.clustering(nx_net)
    clustering_coefficient_df = pd.DataFrame.from_dict(
        clustering_coefficient, orient='index', columns=['clustering_coefficient'])
    clustering_coefficient_df.index.name = 'node'
    clustering_coefficient_df.to_csv(f'{layer}_clustering_coefficient_{threshold}.csv')
    print(f"clustering coefficient for layer {layer} is done!")




def add_edge(row, network, threashold):
    if row['Interactor_A'] != row['Interactor_B']:
        confidence_value = row['Confidence_Value']
        if confidence_value >= threashold:
            network[row['Interactor_A'], row['Interactor_B']] = confidence_value
        else:
            network[row['Interactor_A'], row['Interactor_B']] = 0


def construct_network(data_path, layer_name, threshold=0, centralities=True, percentile=0):

    data = pd.read_csv(data_path)
    confidence_column = data['Confidence_Value']

    threshold = np.percentile(confidence_column, percentile)
    print(f'{layer_name} data read!')

    net = MultilayerNetwork(aspects=0)
    print(f'{layer_name} network constructed!')
    for id in data['Interactor_A']:
        net.add_node(id)
    for id in data['Interactor_B']:
        net.add_node(id)
    print(f'{layer_name} nodes added!')

    data.apply(add_edge, axis=1, args=(net, threshold))
    print(f'{layer_name} edges added!')
    if centralities:
        produce_centralities(net, layer_name, threshold)
        print(f'{layer_name} centralities csv file created!')
    return net


biogrid_path = 'docs/new_biogrid.csv'

construct_network(biogrid_path, 'biogrid', percentile=95)
# intact_path = 'docs/new_intact.csv'
# construct_network(intact_path, 'intact', percentile=95)
# string_path = 'docs/new_string.csv'
# construct_network(string_path, 'string', 600)
