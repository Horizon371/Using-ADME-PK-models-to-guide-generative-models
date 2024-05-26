from tdc.single_pred import ADME
import pandas as pd
from rdkit import Chem


def remove_stereochemistry(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        # Remove stereochemistry
        Chem.RemoveStereochemistry(mol)
        # Return canonical SMILES
        return Chem.MolToSmiles(mol, isomericSmiles=False)
    else:
        return None

data = ADME(name = 'PPBR_AZ')
df = data.get_data()
df['Drug'] = df['Drug'].apply(remove_stereochemistry)

smi_df = pd.read_csv('/home/jovyan/cristian/smiles/sanitizied_smiles_drd2.smi')
smi_list = [item for sublist in smi_df.values.tolist() for item in sublist]

selected_rows = df[df['Drug'].isin(smi_list)]

print(selected_rows)
print(len(selected_rows))