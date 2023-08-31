import pandas as pd
import numpy as np


def func_name():
    return 1


# Create a DataFrame with some missing values (NaN)
data = {
    'A': [1, np.nan, 3],
    'B': ['X', 'Y', np.nan],
    'C': [10, 20, 30]
}

df = pd.DataFrame(data)

# Find rows with NaN values
rows_with_nan = df[pd.isna(df).any(axis=1)]

print("Rows with NaN:")
print(rows_with_nan)

# Convert the DataFrame to a Series and find the NaN cells with their indices
nan_cells = df.stack()[pd.isna(df)].reset_index()

print("\nNaN Cells with Indices:")
print(nan_cells)
