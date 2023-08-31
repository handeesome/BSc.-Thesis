import pandas as pd
import matplotlib.pyplot as plt


def visualization_centrality(centrality_measure):
    # Load the CSV files into DataFrames
    biogrid_data = pd.read_csv(f'docs/biogrid_{centrality_measure}.csv')
    string_data = pd.read_csv(f'docs/string_{centrality_measure}.csv')
    intact_data = pd.read_csv(f'docs/intact_{centrality_measure}.csv')

    # Merge the data based on the 'node' column
    merged_data = biogrid_data.merge(string_data, on='node', how='inner')
    # merged_data['betweenness_centrality'] = 0
    merged_data = merged_data.merge(intact_data, on='node', how='inner')

    sorted_data = merged_data.sort_values(by=f'{centrality_measure}_x', ascending=False)

    # Take only the first 30 nodes
    top_nodes = sorted_data.head(100)

    # Create a scatter plot
    fig, ax = plt.subplots(figsize=(15, 6))

    # Scatter points for each degree centrality
    ax.scatter(top_nodes['node'], top_nodes[f'{centrality_measure}_x'], label='BioGrid', color='blue', alpha=0.5)
    ax.scatter(top_nodes['node'], top_nodes[f'{centrality_measure}_y'], label='STRING', color='green', alpha=0.5)
    ax.scatter(top_nodes['node'], top_nodes[f'{centrality_measure}'], label='IntAct', color='red', alpha=0.5)

    # Add labels and legend
    ax.set_xlabel('Node Names')
    ax.set_ylabel(f'{centrality_measure} Values')
    ax.set_title(f'Scatter Plot of {centrality_measure} across Databases (First 100 Nodes)')
    ax.legend()

    # Rotate x labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Display the plot
    plt.tight_layout()
    plt.savefig(f'images/scatter_plot_{centrality_measure}_biogrid.png', format='png')
    plt.show()


visualization_centrality('clustering_coefficient')
