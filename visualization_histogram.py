import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

biogrid_data = pd.read_csv('docs/biogrid_centralities.csv')
string_data = pd.read_csv('docs/string_centralities.csv')
intact_data = pd.read_csv('docs/intact_centralities.csv')
biogrid_data.replace(0, np.nan, inplace=True)
string_data.replace(0, np.nan, inplace=True)
intact_data.replace(0, np.nan, inplace=True)

# Create subplots for each centrality measure
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Centrality measures
centrality_measures = ['degree_centrality', 'betweenness_centrality', 'closeness_centrality']
centrality_labels = ['Degree Centrality', 'Betweenness Centrality', 'Closeness Centrality']

datasets = [biogrid_data, string_data, intact_data]
dataset_labels = ['BioGRID', 'STRING', 'IntAct']
colors = ['skyblue', 'orange', 'green']

# Plot centrality distribution for each dataset and measure
for dataset, dataset_label, color in zip(datasets, dataset_labels, colors):
    for i, centrality_measure in enumerate(centrality_measures):
        ax = axes[i]
        ax.autoscale(enable=True, axis='x')
        if dataset_label == 'IntAct' and centrality_measure == 'betweenness_centrality':
            continue
        # Filter out NaN values before plotting
        valid_data = dataset[centrality_measure].notna()
        ax.hist(dataset[centrality_measure][valid_data], bins=20, color=color, alpha=0.5, label=dataset_label)
        ax.set_title(centrality_labels[i])
        ax.set_xlabel('Centrality Value')
        ax.set_ylabel('Frequency')
        ax.legend()

# Adjust layout and display plots
plt.tight_layout()
plt.savefig('images/histogram.pdf', format='pdf')
plt.show()
