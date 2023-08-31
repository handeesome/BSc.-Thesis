import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV data into a DataFrame
centrality_data = pd.read_csv('docs/merged_centralities.csv', index_col='node')

# Calculate the correlation matrix between centrality measures for different layers
correlation_matrix = centrality_data.corr(method='pearson')

# Create a heatmap using seaborn
plt.figure(figsize=(10, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt=".2f")
plt.title('Correlation Matrix of Different Thresholds')
plt.tight_layout()
plt.savefig('images/heatmap.png', format='png')
plt.show()
