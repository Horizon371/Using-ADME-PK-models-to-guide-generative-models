import torch
from REINVENT4.reinvent.models.reinvent.models.model import Model
import numpy as np
import pandas as pd

def compute_average_likelihood(model_path, smiles:list):
    model_dict = torch.load(model_path)
    model = Model.create_from_dict(model_dict, "inference", torch.device("cpu"))
    likelihoods = model.likelihood_smiles(smiles)
    return np.mean(likelihoods.data.numpy())
    
def compute_likelihood(model_path, smiles:list):
    model_dict = torch.load(model_path)
    model = Model.create_from_dict(model_dict, "inference", torch.device("cpu"))
    likelihoods = model.likelihood_smiles(smiles)
    return likelihoods.data.numpy().tolist()

#smiles = get_smiles_list("/home/jovyan/cristian/smiles/sanitizied_smiles_drd2.smi") 

# compute_average_likelihood(
#     "/home/jovyan/cristian/outputs/drd2_1__div_IdenticalMurckoScaffold_v2p/andromeda_reinvent.chkpt",
#     smiles
# )

# model_path = "/home/jovyan/cristian/outputs/drd2_0.7_F_0.3__div_ScaffoldSimilarity_v2p_#1/andromeda_reinvent.chkpt"
# smi = pd.read_csv("/home/jovyan/cristian/smiles/drd2_ligands.csv")
# smi["likelihood"] = smi["SMILES"].apply(lambda smiles: compute_likelihood(model_path, smiles))
# print(model_path.split("/")[-2])
# print(smi)