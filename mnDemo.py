from pymnet import *
import pandas as pd
import numpy as np
# def add_edge(row):
#     global network
#     if row['Interactor_A'] != row['Interactor_B']:
#         network[row['Interactor_A'], row['Interactor_B'], row['Interaction_Type'],
#                 row['Interaction_Type']] = row['Confidence_Value']


def add_edge(row, layer):
    global network
    if row['Interactor_A'] != row['Interactor_B']:
        network[row['Interactor_A'], row['Interactor_B'], layer, layer] = row['Confidence_Value']


biogrid_path = 'docs/new_biogrid_demo.csv'
intact_path = 'docs/new_intact_demo.csv'
string_path = 'docs/new_string_demo.csv'
biogrid = pd.read_csv(biogrid_path)
intact = pd.read_csv(intact_path)
string = pd.read_csv(string_path)
# print(len(biogrid))
# print(len(intact))


network = MultilayerNetwork(aspects=1)
for id in biogrid['Interactor_A']:
    network.add_node(id)
for id in biogrid['Interactor_B']:
    network.add_node(id)
for id in intact['Interactor_A']:
    network.add_node(id)
for id in intact['Interactor_B']:
    network.add_node(id)
for id in string['Interactor_A']:
    network.add_node(id)
for id in string['Interactor_B']:
    network.add_node(id)
network.add_layer('biogrid')
network.add_layer('intact')
network.add_layer('string')

biogrid.apply(add_edge, axis=1, args=('biogrid',))
intact.apply(add_edge, axis=1, args=('intact',))
string.apply(add_edge, axis=1, args=('string',))


# print(deg_centrality['Q7JZ62', 'intact'])
# print(deg_centrality['Q7JZ62', 'biogrid'])

deg_distribution = degs(network, degstype="nodes")
print(deg_distribution[(np.nan, 'intact')])
deg_distribution.pop((np.nan, 'intact'))

total_number_nodes = {'biogrid': 2, 'intact': 0, 'string': 0}
keys_to_remove = [key for key, value in deg_distribution.items() if value == 0]
for key in keys_to_remove:
    deg_distribution.pop(key)
deg_centrality = deg_distribution.copy()

for node in deg_distribution:
    total_number_nodes[node[1]] += 1


for layer in total_number_nodes:
    for node in deg_distribution:
        if (node[1] == layer):
            deg_centrality[node] = deg_distribution[node] / (total_number_nodes[layer]-1)
centralities = pd.DataFrame(deg_centrality.items(), columns=['node', 'degree_centrality'])

d, forest = dijkstra(network, list(deg_distribution))
for item in d:
    if (d[item]):
        print(("the node is: " + str(item)) + " and the value is: " + str(d[item]))

# net_density = density(network)
# print("The below is density for this network: ")
# print(net_density)
# count = 0
# for node in deg_centrality:
#     if (deg_centrality[node[0], 'biogrid'] & deg_centrality[node[0], 'intact']):
#         count += 1
# print(count)
# print(deg_centrality)


# print(list(network.A))
# print(len(list(network.A['-'])))
# print(len(list(network.A)))
# print(network.A['MI:0407']['P38624', 'Q7K1C0'])


# degrees = {}
# for layer in network.layers:
#     degrees[layer] = network.degree(layer=layer)
