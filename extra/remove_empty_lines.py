def remove_empty_lines(input_file, output_file):
    # Open the input file for reading
    with open(input_file, 'r') as file_in:
        # Read all lines from the input file
        lines = file_in.readlines()

    # Remove empty lines from the list of lines
    non_empty_lines = [line for line in lines if line.strip()]

    # Open the output file for writing
    with open(output_file, 'w') as file_out:
        # Write the non-empty lines to the output file
        file_out.writelines(non_empty_lines)

# Example usage:
input_file = '/home/jovyan/cristian/scripts/ReinventAndromedaProject/smiles/sanitizied_smiles_no_drd2.smi'
output_file = '/home/jovyan/cristian/scripts/ReinventAndromedaProject/smiles/sanitizied_smiles_no_drd2_no_empty.smi'
remove_empty_lines(input_file, output_file)
print("Empty lines removed successfully.")