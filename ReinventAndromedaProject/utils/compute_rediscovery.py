import pandas as pd

SMI_FILE = "/home/jovyan/cristian/smiles/sanitizied_smiles_drd2.smi"
FOLDER_PATH = "/home/jovyan/cristian/outputs/drd2"


def compute_rediscovery(smi_file, generated_smiles_folder):
    smi = pd.read_csv(smi_file, header=None, names=["SMILES"])
    generated = pd.read_csv(generated_smiles_folder + "/staged_learning_1.csv")
    existing_columns = list(set(generated.columns) & set(["SMILES", "drd2", "step", "fabs", "fdiss", "clint", "vss"]))
    generated = generated[existing_columns]
    overlapping_rows = pd.merge(smi, generated, how='inner', on="SMILES")
    overlapping_rows.drop_duplicates(subset=["SMILES"], keep="first", inplace=True)
    overlapping_rows = overlapping_rows.sort_values(by="drd2", ascending=False)
    overlapping_rows = overlapping_rows.reset_index(drop=True)
    overlapping_rows.to_csv(f'{generated_smiles_folder}/rediscovered.csv', index=False)
    print(overlapping_rows)
    


#compute_rediscovery(SMI_FILE, FOLDER_PATH)