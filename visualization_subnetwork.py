import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load your degree centrality data from CSV files
biogrid_data = pd.read_csv('docs/biogrid_degree_centrality.csv')
string_data = pd.read_csv('docs/string_degree_centrality.csv')

# Define a threshold for high centrality values
high_centrality_threshold = 0.8  # Adjust as needed

# Filter nodes with high centrality values in BioGrid layer
high_centrality_nodes_biogrid = biogrid_data[biogrid_data['degree_centrality'] > high_centrality_threshold]['node']

# Create a NetworkX graph for BioGrid layer
biogrid_graph = nx.Graph()

# Add nodes to the graph
biogrid_graph.add_nodes_from(high_centrality_nodes_biogrid)

# Create edges as needed based on your data

# Create a sub-network visualization for BioGrid layer
plt.figure(figsize=(8, 6))
pos_biogrid = nx.spring_layout(biogrid_graph)
nx.draw(biogrid_graph, pos_biogrid, with_labels=True, font_size=8, font_color='black', node_size=200)
plt.title('Sub-network Visualization for BioGrid Layer')
plt.show()

# # Similar steps for the STRING layer
# # Filter nodes with high centrality values in STRING layer
# high_centrality_nodes_string = string_data[string_data['degree_centrality'] > high_centrality_threshold]['node']

# # Create a NetworkX graph for STRING layer
# string_graph = nx.Graph()

# # Add nodes to the graph
# string_graph.add_nodes_from(high_centrality_nodes_string)

# # Create edges as needed based on your data

# # Create a sub-network visualization for STRING layer
# plt.figure(figsize=(8, 6))
# pos_string = nx.spring_layout(string_graph)
# nx.draw(string_graph, pos_string, with_labels=True, font_size=8, font_color='black', node_size=200)
# plt.title('Sub-network Visualization for STRING Layer')
# plt.show()
