import pandas as pd
import matplotlib.pyplot as plt

# Load your data from CSV files
biogrid_data = pd.read_csv('docs/biogrid_centralities.csv')
string_data = pd.read_csv('docs/string_centralities.csv')
intact_data = pd.read_csv('docs/intact_centralities.csv')

merged_data = pd.read_csv('docs/merged_closeness_centrality.csv')
merged_data['average_closeness_centrality'] = merged_data[
    ['biogrid_closeness_centrality', 'string_closeness_centrality', 'intact_closeness_centrality']
].mean(axis=1)
node_with_highest_average_cc = merged_data.loc[
    merged_data['average_closeness_centrality'].idxmax()
]['node']
merged_data = pd.read_csv('docs/merged_degree_centrality.csv')
highest_biogrid_node = merged_data.loc[merged_data['biogrid_degree_centrality'].idxmax(), 'node']
# highest_intact_node = merged_data.loc[merged_data['intact_degree_centrality'].idxmax(), 'node']

# Choose specific nodes to compare
nodes_to_compare = ['Q5VV41', highest_biogrid_node, node_with_highest_average_cc
                    ]  # Replace with actual node names

# Initialize lists to store centrality values for each node and measure
degree_centralities = []
betweenness_centralities = []
closeness_centralities = []

# Iterate through each node
for node in nodes_to_compare:
    print(node)
    # Retrieve centrality values for each layer and measure
    degree_centralities.append({
        'BioGrid': biogrid_data[biogrid_data['node'] == node]['degree_centrality'].values[0],
        'STRING': string_data[string_data['node'] == node]['degree_centrality'].values[0],
        'IntAct': intact_data[intact_data['node'] == node]['degree_centrality'].values[0]
    })

    betweenness_centralities.append({
        'BioGrid': biogrid_data[biogrid_data['node'] == node]['betweenness_centrality'].values[0],
        'STRING': string_data[string_data['node'] == node]['betweenness_centrality'].values[0],
        'IntAct': intact_data[intact_data['node'] == node]['betweenness_centrality'].values[0]
    })

    closeness_centralities.append({
        'BioGrid': biogrid_data[biogrid_data['node'] == node]['closeness_centrality'].values[0],
        'STRING': string_data[string_data['node'] == node]['closeness_centrality'].values[0],
        'IntAct': intact_data[intact_data['node'] == node]['closeness_centrality'].values[0]
    })

# Convert the centrality data to DataFrames
degree_df = pd.DataFrame(degree_centralities, index=nodes_to_compare)
betweenness_df = pd.DataFrame(betweenness_centralities, index=nodes_to_compare)
closeness_df = pd.DataFrame(closeness_centralities, index=nodes_to_compare)

# Create bar charts or radar charts
plt.figure(figsize=(12, 8))

# Bar charts for degree centrality
plt.subplot(3, 1, 1)
degree_df.plot(kind='bar', ax=plt.gca())
plt.title('Comparison of Degree Centrality across Layers')
plt.ylabel('Degree Centrality')

# Bar charts for betweenness centrality
plt.subplot(3, 1, 2)
betweenness_df.plot(kind='bar', ax=plt.gca())
plt.title('Comparison of Betweenness Centrality across Layers')
plt.ylabel('Betweenness Centrality')

# Bar charts for closeness centrality
plt.subplot(3, 1, 3)
closeness_df.plot(kind='bar', ax=plt.gca())
plt.title('Comparison of Closeness Centrality across Layers')
plt.ylabel('Closeness Centrality')

plt.tight_layout()
plt.savefig('images/centrality_comparison.png', format='png')
plt.show()
