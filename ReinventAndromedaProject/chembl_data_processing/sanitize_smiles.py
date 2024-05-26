import pandas as pd
from rdkit import Chem
from rdkit.Chem.SaltRemover import SaltRemover

def sanitize_smiles(df, smiles_column, allowed_atoms):
    """
    This function does three things:
    - Filter out SMILES that contain other elements than the ones allowed
    - Remove streochemistry information
    - Remove salts
    """
    filtered_smiles = []
    for smiles in df[smiles_column]:
        mol = Chem.MolFromSmiles(smiles)
        if mol is not None:
            contains_allowed_atoms = all(atom.GetSymbol() in allowed_atoms for atom in mol.GetAtoms())
            if contains_allowed_atoms:
                remover = SaltRemover()
                stripped = remover.StripMol(mol)
                Chem.RemoveStereochemistry( stripped ) 
                filtered_smiles.append(Chem.MolToSmiles(stripped))
    return filtered_smiles


df = pd.read_csv('/home/jovyan/cristian/scripts/ReinventAndromedaProject/smiles/drd2_pchembl_5.csv')
allowed_atoms = ['H', 'C', 'N', 'O', 'F', 'S', 'Cl', 'Br']
sanitized_smiles = sanitize_smiles(df, "canonical_smiles", allowed_atoms)

with open('/home/jovyan/cristian/scripts/ReinventAndromedaProject/smiles/sanitizied_smiles_drd2.smi', 'w') as f:
    for smiles in sanitized_smiles:
        f.write(smiles + '\n')

print("Filtered SMILES have been saved to 'sanitizied_smiles.smi'.")