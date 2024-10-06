import pandas as pd

# Load the two Excel files
file1 = 'cnfile.xlsx'
file2 = 'cdfile.xlsx'

# Read the Excel files into DataFrames
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# Merge the DataFrames column-wise
merged_df = pd.concat([df1, df2], axis=1)

# Save the merged DataFrame to a new Excel file
merged_df.to_excel('merged_file.xlsx', index=False)

print("Files merged successfully!")
