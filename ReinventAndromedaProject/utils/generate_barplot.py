import matplotlib.pyplot as plt
import numpy as np
from likelihood_of_smiles import *

# def compute_lists(experiments):
#     averages = []
#     standard_deviations = []
#     smi = get_smiles_list("/home/jovyan/cristian/smiles/sanitizied_smiles_drd2_copy.smi")
    
#     for experiment in experiments:
#         results = []
#         for measurement in experiment:
#             #model_path = f"{measurement}/andromeda_reinvent.chkpt"
#             #result = compute_average_likelihood(model_path, smi)
#             result = get_number_of_rediscoveries(measurement)
#             print(measurement, result)
#             results.append(result)
#         avg, std = create_average_and_std(results)
#         averages.append(avg)
#         standard_deviations.append(std)
        
#     return averages, standard_deviations    

def compute_lists(experiments):
    averages = []
    standard_deviations = []
    smi = get_smiles_list("/home/jovyan/cristian/smiles/sanitizied_smiles_drd2_copy.smi")
    
    df = pd.read_csv("/home/jovyan/cristian/NLL_models.csv")
    print(df)
    likelihoods = df["nll"].tolist()
    likelihods_split =  [likelihoods[i:i + 3] for i in range(0, len(likelihoods), 3)]
    
    for experiment in likelihods_split:
        avg, std = create_average_and_std(experiment)
        averages.append(avg)
        standard_deviations.append(std)
        
    return averages, standard_deviations


def get_smiles_list(smi_file):
    smi = pd.read_csv(smi_file, header=None, names=["SMILES"])
    return smi["SMILES"].tolist()

def get_number_of_rediscoveries(measurement):
    rediscovered = pd.read_csv(f"{measurement}/rediscovered.csv")
    return len(rediscovered)
    
def create_average_and_std(measurement_results):
    avg = sum(measurement_results) / 3 
    std = np.std(measurement_results) / np.sqrt(3)
    return avg, std
    

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
    ["/home/jovyan/cristian/outputs/drd2_0.6_fabs_0.1_fdiss_0.1_clint_0.1_vss_0.1_V2P",
     "/home/jovyan/cristian/outputs/drd2_0.6_fabs_0.1_fdiss_0.1_clint_0.1_vss_0.1_V2P_#2",
     "/home/jovyan/cristian/outputs/drd2_0.6_fabs_0.1_fdiss_0.1_clint_0.1_vss_0.1_V2P_#3"],
    ["/home/jovyan/cristian/outputs/drd2_0.7_F_0.3_#3__div_ScaffoldSimilarity_v2p_#2",
     "/home/jovyan/cristian/outputs/drd2_0.7_F_0.3_#3__div_ScaffoldSimilarity_v2p_#3",
     "/home/jovyan/cristian/outputs/drd2_0.7_F_0.3_#3__div_ScaffoldSimilarity_v2p_#4"]
]

#indices = ["DRD2", "+Fabs", "+Fdiss", "+Vss", "+Clint", "All"]
indices = ["DRD2", r'+$f_{abs}$', r'+$f_{diss}$',  r'+$V_{ss}$', r'+$CL_{int}$', "+all", "+F", ]


# experiments=[
#     ["/home/jovyan/cristian/outputs/drd2_1__div_ScaffoldSimilarity_v2p",
#      "/home/jovyan/cristian/outputs/drd2_1__div_ScaffoldSimilarity_v2p_#2",
#      "/home/jovyan/cristian/outputs/drd2_1__div_ScaffoldSimilarity_v2p_#3"],
#     ["/home/jovyan/cristian/outputs/drd2_1__div_IdenticalMurckoScaffold_v2p",
#      "/home/jovyan/cristian/outputs/drd2_1__div_IdenticalMurckoScaffold_v2p_#2",
#      "/home/jovyan/cristian/outputs/drd2_1__div_IdenticalMurckoScaffold_v2p_#3"],
#     ["/home/jovyan/cristian/outputs/drd2_1__div_IdenticalTopologicalScaffold_v2p",
#      "/home/jovyan/cristian/outputs/drd2_1__div_IdenticalTopologicalScaffold_v2p_#2",
#      "/home/jovyan/cristian/outputs/drd2_1__div_IdenticalTopologicalScaffold_v2p_#3"]
# ]

#indices = ["ScaffoldSimilarity", "Murcko", "Topological"]

averages, standard_deviations = compute_lists(experiments)

colors = ['steelblue', 'salmon','tan', 'lightseagreen', 'peru', 'violet', 'darkorange']

plt.figure(figsize=(8, 6))  # Increase the width to make the x-axis larger
plt.bar(indices, averages, yerr=standard_deviations, color=colors, capsize=15)
plt.xlabel('RL Agents', fontsize=16)
plt.ylabel('Average NLL of DRD2 bioactives', fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16, length=4, width=2)
plt.show()


result_string = '_'.join(indices)

plt.savefig(f'all_barplot_F_nll_2.png')
