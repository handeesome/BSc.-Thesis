import networkx as nx
from networkx.algorithms import bipartite
G = nx.MultiLayerGraph()
layers = ['layer1', 'layer2', 'layer3']
nodes = ['node1', 'node2', 'node3']

for layer in layers:
    G.add_layer(layer)

for node in nodes:
    for layer in layers:
        G.add_node(node, layer=layer)
G.add_edge('node1', 'node2', layer=('layer1', 'layer2'))
G.add_edge('node2', 'node3', layer=('layer2', 'layer3'))
# Add more edges as needed
