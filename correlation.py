import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt


def pearson_correlation(measure):
    # Load the CSV files into DataFrames
    biogrid_data = pd.read_csv(f'docs/biogrid_{measure}.csv')
    string_data = pd.read_csv(f'docs/string_{measure}.csv')
    intact_data = pd.read_csv(f'docs/intact_{measure}.csv')

    # Merge the data based on the 'node' column
    merged_data_biogrid_string = biogrid_data.merge(string_data, on='node', how='inner')
    print(f'The length of merged_data_biogrid_string is {len(merged_data_biogrid_string)}')
    merged_data_biogrid_intact = biogrid_data.merge(intact_data, on='node', how='inner')
    print(f'The length of merged_data_biogrid_intact is {len(merged_data_biogrid_intact)}')
    merged_data_string_intact = string_data.merge(intact_data, on='node', how='inner')
    print(f'The length of merged_data_string_intact is {len(merged_data_string_intact)}')

    # Calculate the Pearson's correlation coefficients
    correlation_biogrid_string, _ = pearsonr(
        merged_data_biogrid_string[f'{measure}_x'],
        merged_data_biogrid_string[f'{measure}_y'])
    correlation_biogrid_intact, _ = pearsonr(
        merged_data_biogrid_intact[f'{measure}_x'],
        merged_data_biogrid_intact[f'{measure}_y'])
    correlation_string_intact, _ = pearsonr(
        merged_data_string_intact[f'{measure}_x'],
        merged_data_string_intact[f'{measure}_y'])

    # Print the correlation coefficients
    print(
        f"Pearson's correlation coefficient on {measure} between BioGrid and STRING: {correlation_biogrid_string:.3f}")
    print(
        f"Pearson's correlation coefficient on {measure} between BioGrid and IntAct: {correlation_biogrid_intact:.3f}")
    print(f"Pearson's correlation coefficient on {measure} between STRING and IntAct: {correlation_string_intact:.3f}")


pearson_correlation('clustering_coefficient')
