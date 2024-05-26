import pandas as pd
from rdkit import Chem
from rdkit.Chem.SaltRemover import SaltRemover

df = pd.read_csv("/home/jovyan/cristian/smiles/drd2_ligands.csv")

def remove_stereochemistry(smiles):
    mol = Chem.MolFromSmiles(smiles)
    Chem.RemoveStereochemistry(mol) 
    return Chem.MolToSmiles(mol)
     

df['SMILES'] = df['SMILES'].apply(remove_stereochemistry)
df.to_csv("drd2_ligands_ns.csv", index=False)
