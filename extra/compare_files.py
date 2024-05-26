
import pandas as pd

def compare_files(file1_path, file2_path):
    # Read the files into pandas DataFrames
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    # Find overlapping rows
    overlapping_rows = pd.merge(df1, df2, how='inner', on="canonical_smiles")

    # Display overlapping rows
    print("Overlapping Rows:")
    overlapping_rows.to_csv("scripts/ReinventAndromedaProject/overlap_filtered_to_drd2.csv", index=False)

# File paths
file1_path = 'scripts/ReinventAndromedaProject/filtered_out_drd2.csv'
file2_path = 'scripts/ReinventAndromedaProject/result_file.csv'

def negative_intersection(file1_path, file2_path):
    # Read the files into pandas DataFrames
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    # Perform a left join to find rows in df1 not present in df2
    neg_intersection_df = pd.merge(df1, df2[["canonical_smiles"]], how='left', on="canonical_smiles", indicator=True)
    neg_intersection_df = neg_intersection_df[neg_intersection_df['_merge'] == 'left_only']

    # Drop the indicator column
    neg_intersection_df.drop('_merge', axis=1, inplace=True)

    # Save the negative intersection DataFrame to a new CSV file
    neg_intersection_df.to_csv("scripts/ReinventAndromedaProject/overlap_filtered_to_drd2.csv", index=False)
# 
# Compare files
#compare_files(file1_path, file2_path)

df = pd.read_csv('scripts/ReinventAndromedaProject/result_file.csv')
filtered_df = df[df["compound_chembl_id"] == "CHEMBL1202214"]

filtered_df.to_csv('duplicates.csv', index=False)
