import random

def split_smiles_file(input_file, train_file, validation_file, split_ratio=0.8, seed=None):
    # Read SMILES from the input file
    with open(input_file, 'r') as f:
        smiles = f.readlines()

    # Shuffle the SMILES
    if seed is not None:
        random.seed(seed)
    random.shuffle(smiles)

    # Split the SMILES into training and validation sets
    split_index = int(len(smiles) * split_ratio)
    train_smiles = smiles[:split_index]
    validation_smiles = smiles[split_index:]

    # Write the training set to the train file
    with open(train_file, 'w') as f_train:
        f_train.writelines(train_smiles)

    # Write the validation set to the validation file
    with open(validation_file, 'w') as f_validation:
        f_validation.writelines(validation_smiles)

# Example usage:
input_file = '/home/jovyan/cristian/scripts/ReinventAndromedaProject/smiles/sanitizied_smiles_no_drd2_no_empty.smi'
train_file = '/home/jovyan/cristian/scripts/ReinventAndromedaProject/smiles/train_set.smi' 
validation_file = '/home/jovyan/cristian/scripts/ReinventAndromedaProject/smiles/validation_set.smi'
split_ratio = 0.9

split_smiles_file(input_file, train_file, validation_file, split_ratio)
print("SMILES file split into training and validation sets successfully.")