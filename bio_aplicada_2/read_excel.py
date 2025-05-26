import pandas as pd

# Read the Excel file into a pandas DataFrame
file_path = 'Codon_aa_table.xlsx'
df = pd.read_excel(file_path)

# Display the first few rows of the DataFrame
print(df.head())