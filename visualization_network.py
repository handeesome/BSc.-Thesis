from pymnet import *
import matplotlib
import pandas as pd
matplotlib.use('TkAgg')


def find_clustering_center():
    biogrid_data = pd.read_csv('docs/biogrid_degree_centrality.csv')
    string_data = pd.read_csv('docs/string_degree_centrality.csv')
    intact_data = pd.read_csv('docs/intact_degree_centrality.csv')
    merged_data = biogrid_data.merge(string_data, on='node', how='inner')
    merged_data = merged_data.merge(intact_data, on='node', how='inner')
    merged_data['average_degree_centrality'] = merged_data[
        ['degree_centrality_x', 'degree_centrality_y', 'degree_centrality']
    ].mean(axis=1)

    # Find the node with the highest average degree centrality
    node_with_highest_average = merged_data.loc[
        merged_data['average_degree_centrality'].idxmax()
    ]['node']

    return node_with_highest_average


def find_node_pairs(clustering_center, data_path, first_layer, second_layer):

    dataPath = data_path
    df = pd.read_csv(dataPath)

    # Initialize a list to store pairs of nodes
    node_pairs = []

    # Add the pair of the most clustered node with itself
    node_pairs.append((clustering_center, clustering_center))

    # Initialize a dictionary to keep track of the number of pairs for each node
    node_pair_count = 0

    # Add the nodes involving the most clustered node from Interactor_A and Interactor_B
    nodes_involving_most_clustered = []
    nodes_involving_most_clustered.extend(df.loc[
        (df['Interactor_B'] == clustering_center), 'Interactor_A'
    ])
    nodes_involving_most_clustered.extend(df.loc[
        (df['Interactor_A'] == clustering_center), 'Interactor_B'
    ])
    # Loop through the nodes involving the most clustered node
    for node in nodes_involving_most_clustered[:first_layer].copy():

        nodes_involving_node = []
        nodes_involving_node.extend(df.loc[
            (df['Interactor_B'] == node), 'Interactor_A'
        ])
        nodes_involving_node.extend(df.loc[
            (df['Interactor_A'] == node), 'Interactor_B'
        ])
        nodes_involving_most_clustered.extend(nodes_involving_node)
        # Add the pair of the node and the most clustered node to the list
        node_pairs.append((node, clustering_center))
        # Add the pair of the node and its involved nodes to the list
        for involved_node in nodes_involving_node[:second_layer]:
            # if node_pair_count >= second_layer:
            #     node_pair_count = 0
            #     break  # Stop adding pairs if the limit is reached
            node_pairs.append((node, involved_node))
            node_pair_count += 1

    return node_pairs


def add_edge(Interactor_A, Interactor_B, layer):
    global network
    if Interactor_A != Interactor_B:
        network[Interactor_A, Interactor_B, layer, layer] = 1


biogrid_data_path = 'docs/new_biogrid.csv'
clustering_center = find_clustering_center()
biogrid_pairs = find_node_pairs(clustering_center, biogrid_data_path, 5, 5)
# print(len(biogrid_pairs))
intact_data_path = 'docs/new_intact.csv'
intact_pairs = find_node_pairs(clustering_center, intact_data_path, 5, 5)
# print(len(intact_pairs))
string_data_path = 'docs/new_string.csv'
string_pairs = find_node_pairs(clustering_center, string_data_path, 5, 5)
# biogrid_data_path = 'docs/new_biogrid.csv'
# biogrid_clusterco_path = 'docs/biogrid_clustering_coefficient.csv'
# print(len(find_node_pairs(biogrid_clusterco_path, biogrid_data_path)))

all_nodes = set()
all_nodes.update([pair[0] for pair in biogrid_pairs])
all_nodes.update([pair[1] for pair in biogrid_pairs])
all_nodes.update([pair[0] for pair in intact_pairs])
all_nodes.update([pair[1] for pair in intact_pairs])
all_nodes.update([pair[0] for pair in string_pairs])
all_nodes.update([pair[1] for pair in string_pairs])

# Create a mapping of unique node names to ordered numbers
node_name_to_number = {node: number for number, node in enumerate(all_nodes)}

# Replace node names in biogrid_pairs, intact_pairs, and string_pairs with ordered numbers
biogrid_pairs_mapped = [(node_name_to_number[pair[0]], node_name_to_number[pair[1]]) for pair in biogrid_pairs]
intact_pairs_mapped = [(node_name_to_number[pair[0]], node_name_to_number[pair[1]]) for pair in intact_pairs]
string_pairs_mapped = [(node_name_to_number[pair[0]], node_name_to_number[pair[1]]) for pair in string_pairs]


# Loop through the mapped pairs and add edges to the network
network = MultilayerNetwork(aspects=1)


def draw_network(node):
    if node == 'numbers':
        for pair in biogrid_pairs_mapped:
            add_edge(pair[0], pair[1], 'biogrid')
        for pair in intact_pairs_mapped:
            add_edge(pair[0], pair[1], 'intact')
        for pair in string_pairs_mapped:
            add_edge(pair[0], pair[1], 'string')

        fig = draw(network, autoscale=True, alignedNodes=True, layout='spring')
        fig.savefig("images/network_numbers.png", format='png')
    elif node == 'ids':
        for pair in biogrid_pairs:
            add_edge(pair[0], pair[1], 'biogrid')
        for pair in intact_pairs:
            add_edge(pair[0], pair[1], 'intact')
        for pair in string_pairs:
            add_edge(pair[0], pair[1], 'string')

        fig = draw(network, autoscale=True, alignedNodes=True, layout='spring')
        fig.savefig("images/network_ids.png")


draw_network('numbers')
