import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data into a DataFrame
clustering_data = pd.read_csv('docs/merged_clustering_coefficient.csv')

# Plot the distribution of clustering coefficients for each layer
plt.figure(figsize=(10, 6))

# Loop through the columns corresponding to each layer
for layer in clustering_data.columns[1:]:
    layer_data = clustering_data[layer]
    plt.hist(layer_data, bins=10, alpha=0.5, label=layer)

plt.title('Distribution of Clustering Coefficients by Layer')
plt.xlabel('Clustering Coefficient')
plt.ylabel('Frequency')
plt.legend()
plt.savefig('images/clutering.pdf', format='pdf')
plt.show()
