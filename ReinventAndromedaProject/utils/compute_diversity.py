from rdkit import Chem
from rdkit.Chem import AllChem
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
import os, statistics


SAMPLE_SIZE = 1850
FOLDER_PATH = "/home/jovyan/cristian/outputs/drd2_1__div_ScaffoldSimilarity_v2p"

def read_smiles_from_file(file_path):
    df = pd.read_csv(file_path, usecols=["SMILES"])
    smiles = df[~df["SMILES"].str.contains("INVALID")]
    sampled_smiles = smiles.sample(n=SAMPLE_SIZE, random_state=42)
    smiles_list = sampled_smiles.values.tolist()
    return smiles_list

def calculate_tanimoto_similarity(smiles_1, smiles_2):
    mol_1 = Chem.MolFromSmiles(smiles_1[0])
    mol_2 = Chem.MolFromSmiles(smiles_2[0])
    if mol_1 is not None and mol_2 is not None:
        fp_1 = AllChem.GetMorganFingerprint(mol_1, 2)
        fp_2 = AllChem.GetMorganFingerprint(mol_2, 2)
        return AllChem.DataStructs.TanimotoSimilarity(fp_1, fp_2)
    else:
        return None

def average_pairwise_tanimoto_similarity(smiles_list):
    pairs = itertools.combinations(smiles_list, 2)
    similiarities = []
    for pair in pairs:
        similarity = calculate_tanimoto_similarity(pair[0], pair[1])
        similiarities.append(similarity)
    return similiarities

def plot_pairwise_similarity(similiarities, folder_path):
    plt.figure(figsize=(10, 6))  # Increase the width to make the x-axis larger
    plt.xlabel('Similarity', fontsize=14)
    plt.yscale('log')
    plt.ylabel('log Frequencies', fontsize=14)
    sns.histplot(similiarities, kde=False, bins=40, color='orange')
    plt.title(f'Avg: {"{:.4f}".format(statistics.mean(similiarities))}, Median: {"{:.4f}".format(statistics.median(similiarities))}, Sample: {SAMPLE_SIZE}',
              fontsize=14)
    plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    plt.gca().set_ylim(bottom=0)
    plt.tick_params(axis='both', which='major', labelsize=14, length=2, width=1)
    histogram_save_path = f"{folder_path}/pairwise_similarities"
    if not os.path.exists(histogram_save_path): 
        os.makedirs(histogram_save_path)
    

    last_subfolder = folder_path.split('/')[-1]
    
    plt.savefig(f'{histogram_save_path}/similiarity_{SAMPLE_SIZE}_{last_subfolder}.png')

def compute_and_plot_pairwise_similarities(generated_smiles_folder):
    file_path = f"{generated_smiles_folder}/staged_learning_1.csv"
    smiles_list = read_smiles_from_file(file_path)
    similarities = average_pairwise_tanimoto_similarity(smiles_list)
    plot_pairwise_similarity(similarities, generated_smiles_folder)

#compute_and_plot_pairwise_similarities(FOLDER_PATH)