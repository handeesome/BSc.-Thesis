import pandas as pd

# deg = pd.read_csv('docs/string_degree_centrality_600.csv')
# btns = pd.read_csv('docs/string_betweenness_centrality_600.csv')[['node', 'betweenness_centrality']]
# cc = pd.read_csv('docs/string_closeness_centrality_600.csv')
# clusterco = pd.read_csv('docs/string_clustering_coefficient_600.csv')

# # intact_betweenness = pd.read_csv('docs/intact_degree_centrality.csv')
# deg.rename(columns={'degree_centrality': 'degree_centrality_600'}, inplace=True)
# btns.rename(columns={'betweenness_centrality': 'betweenness_centrality_600'}, inplace=True)
# cc.rename(columns={'closeness_centrality': 'closeness_centrality_600'}, inplace=True)
# clusterco.rename(columns={'clustering_coefficient': 'clustering_coefficient_600'}, inplace=True)
# merged_data = deg.merge(btns, on='node', how='inner')
# merged_data = merged_data.merge(cc, on='node', how='inner')
# merged_data = merged_data.merge(clusterco, on='node', how='inner')
# merged_data.to_csv('docs/string_centralities_600.csv', index=False)

zero = pd.read_csv('docs/string_centralities.csv')
low = pd.read_csv('docs/string_centralities_600.csv')
high = pd.read_csv('docs/string_centralities_850.csv')
merged_data = zero.merge(low, on='node', how='inner')
merged_data = merged_data.merge(high, on='node', how='inner')
merged_data.to_csv('docs/merged_string_thresholds.csv', index=False)
