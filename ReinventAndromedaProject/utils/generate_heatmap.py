import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from likelihood_of_smiles import *

models = ["DRD2", r'$f_{abs}$', r'$f_{diss}$',  r'$V_{ss}$', r'$CL_{int}$', "F", "all"]

experiments=[
    ["/home/jovyan/cristian/outputs/drd2_1__div_ScaffoldSimilarity_v2p",
     "/home/jovyan/cristian/outputs/drd2_1__div_ScaffoldSimilarity_v2p_#2",
     "/home/jovyan/cristian/outputs/drd2_1__div_ScaffoldSimilarity_v2p_#3"],
    ["/home/jovyan/cristian/outputs/drd2_0.7_fabs_0.3_div_ScaffoldSimiliarty_V2P",
     "/home/jovyan/cristian/outputs/drd2_0.7_fabs_0.3_div_ScaffoldSimiliarty_V2P_#2",
     "/home/jovyan/cristian/outputs/drd2_0.7_fabs_0.3_div_ScaffoldSimiliarty_V2P_#3"],
    ["/home/jovyan/cristian/outputs/drd2_0.7_fdiss_0.3_div_ScaffoldSimiliarty_V2P",
      "/home/jovyan/cristian/outputs/drd2_0.7_fdiss_0.3_div_ScaffoldSimiliarty_V2P_#2",
      "/home/jovyan/cristian/outputs/drd2_0.7_fdiss_0.3_div_ScaffoldSimiliarty_V2P_#3"],
    ["/home/jovyan/cristian/outputs/drd2_0.7_vss_0.3_div_ScaffoldSimiliarty_V2P",
     "/home/jovyan/cristian/outputs/drd2_0.7_vss_0.3_div_ScaffoldSimiliarty_V2P_#2",
     "/home/jovyan/cristian/outputs/drd2_0.7_vss_0.3_div_ScaffoldSimiliarty_V2P_#3"],
    ["/home/jovyan/cristian/outputs/drd2_0.7_clint_0.3_div_ScaffoldSimiliarty_V2P",
     "/home/jovyan/cristian/outputs/drd2_0.7_clint_0.3_div_ScaffoldSimiliarty_V2P_#2",
     "/home/jovyan/cristian/outputs/drd2_0.7_clint_0.3_div_ScaffoldSimiliarty_V2P_#3"],
    ["/home/jovyan/cristian/outputs/drd2_0.7_F_0.3_#3__div_ScaffoldSimilarity_v2p_#2",
     "/home/jovyan/cristian/outputs/drd2_0.7_F_0.3_#3__div_ScaffoldSimilarity_v2p_#3",
     "/home/jovyan/cristian/outputs/drd2_0.7_F_0.3_#3__div_ScaffoldSimilarity_v2p_#4"],
    ["/home/jovyan/cristian/outputs/drd2_0.6_fabs_0.1_fdiss_0.1_clint_0.1_vss_0.1_V2P",
     "/home/jovyan/cristian/outputs/drd2_0.6_fabs_0.1_fdiss_0.1_clint_0.1_vss_0.1_V2P_#2",
     "/home/jovyan/cristian/outputs/drd2_0.6_fabs_0.1_fdiss_0.1_clint_0.1_vss_0.1_V2P_#3"]
]

def create_average_and_std(experiment_likelihoods):
    avg_likelihoods = []
    for l1, l2, l3 in zip(experiment_likelihoods[0], experiment_likelihoods[1], experiment_likelihoods[2]):
        average = (l1 + l2 + l3)/3
        avg_likelihoods.append(average)
    return avg_likelihoods

def generate_dataset():
    likelihoods = []
    compound_list = compounds["SMILES"].tolist()

    for experiment in experiments:
        experiment_likelihoods = []
        for measurement in experiment:
            model_path = f"{measurement}/andromeda_reinvent.chkpt"
            result = compute_likelihood(model_path, compound_list)
            experiment_likelihoods.append(result)
            #print(measurement)
            #print(compounds["name"].tolist())
            #print(result)
            #print(" ")

        avg_likelihoods = create_average_and_std(experiment_likelihoods)
        likelihoods.append(avg_likelihoods)
                
    return likelihoods
    

def generate_plot(data):
    # Create the heatmap
    plt.figure(figsize=(10, 8))
    h = sns.heatmap(data, annot=True, cmap='viridis_r', yticklabels=compounds["name"].tolist(), annot_kws={"fontsize":13})
    #ticks = h.get_xticks()  # Get current tick locations
    #font_properties = [{'fontsize': 14}, {'fontsize': 18}, {'fontsize': 18}, {'fontsize': 18}, {'fontsize': 10}, {'fontsize': 10}, {'fontsize': 10}, {'fontsize': 10}, {'fontsize': 10}]
    h.set_xticklabels(models, size = 15)
    h.tick_params(axis='x', pad=7)  # Adjust 'x' to 'y' for the y-axis
    h.set_yticklabels(compounds["name"].tolist(), fontsize=13, rotation=0)
    colorbar = h.collections[0].colorbar
    colorbar.ax.tick_params(labelsize=12)
    plt.tight_layout()  # Adjust layout to be tight
    plt.subplots_adjust(left=0.18)  # Increase the left margin
    plt.savefig("heatmap")
    plt.show()
    
compounds = pd.read_csv("/home/jovyan/cristian/smiles/drd2_ligands.csv") 
likelihoods = generate_dataset()
A = np.array(likelihoods)
generate_plot(A.T)