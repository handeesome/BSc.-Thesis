import pandas as pd
import matplotlib.pyplot as plt


def visualization_centrality(db, centrality_measure):
    # Load the CSV files into DataFrames
    normal = pd.read_csv(f'docs/{db}_{centrality_measure}.csv')
    low_threshold = pd.read_csv(f'docs/{db}_{centrality_measure}_600.csv')
    high_threshold = pd.read_csv(f'docs/{db}_{centrality_measure}_850.csv')

    # Merge the data based on the 'node' column
    merged_data = normal.merge(low_threshold, on='node', how='inner')
    merged_data = merged_data.merge(high_threshold, on='node', how='inner')

    sorted_data = merged_data.sort_values(by=f'{centrality_measure}_y', ascending=False)

    # Take only the first 30 nodes
    top_nodes = sorted_data.head(100)

    # Create a scatter plot
    fig, ax = plt.subplots(figsize=(15, 6))

    # Scatter points for each degree centrality
    ax.scatter(top_nodes['node'], top_nodes[f'{centrality_measure}_x'], label='0', color='blue', alpha=0.5)
    ax.scatter(top_nodes['node'], top_nodes[f'{centrality_measure}_y'], label='600', color='green', alpha=0.5)
    ax.scatter(top_nodes['node'], top_nodes[f'{centrality_measure}'], label='850', color='red', alpha=0.5)

    # Add labels and legend
    ax.set_xlabel('Node Names')
    ax.set_ylabel(f'{centrality_measure} Values')
    ax.set_title(f'Scatter Plot of {centrality_measure} in {db} for different thresholds (First 100 Nodes)')
    ax.legend()

    # Rotate x labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Display the plot
    plt.tight_layout()
    plt.savefig(f'images/scatter_plot_{db}_{centrality_measure}.png', format='png')
    plt.show()


visualization_centrality('string', 'degree_centrality')
