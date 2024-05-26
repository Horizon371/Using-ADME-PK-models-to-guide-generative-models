import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import subprocess
import json

def run_subprocess(model, input):
    result = subprocess.run(['python3', '/home/jovyan/cristian/scripts/ReinventAndromedaProject/run_andromeda.py', model, 'confidence', '0.7'], input=input, text=True, capture_output=True)
    return result

# experiments=[
#     "/home/jovyan/cristian/outputs/drd2_1__div_ScaffoldSimilarity_v2p",
#     "/home/jovyan/cristian/outputs/drd2_1__div_ScaffoldSimilarity_v2p_#2",
#     "/home/jovyan/cristian/outputs/drd2_1__div_ScaffoldSimilarity_v2p_#3",
    
#     "/home/jovyan/cristian/outputs/drd2_0.7_fabs_0.3_div_ScaffoldSimiliarty_V2P",
#     "/home/jovyan/cristian/outputs/drd2_0.7_fabs_0.3_div_ScaffoldSimiliarty_V2P_#2",
#     "/home/jovyan/cristian/outputs/drd2_0.7_fabs_0.3_div_ScaffoldSimiliarty_V2P_#3",
    
#     "/home/jovyan/cristian/outputs/drd2_0.7_fdiss_0.3_div_ScaffoldSimiliarty_V2P",
#     "/home/jovyan/cristian/outputs/drd2_0.7_fdiss_0.3_div_ScaffoldSimiliarty_V2P_#2",
#     "/home/jovyan/cristian/outputs/drd2_0.7_fdiss_0.3_div_ScaffoldSimiliarty_V2P_#3",
    
#     "/home/jovyan/cristian/outputs/drd2_0.7_vss_0.3_div_ScaffoldSimiliarty_V2P",
#     "/home/jovyan/cristian/outputs/drd2_0.7_vss_0.3_div_ScaffoldSimiliarty_V2P_#2",
#     "/home/jovyan/cristian/outputs/drd2_0.7_vss_0.3_div_ScaffoldSimiliarty_V2P_#3",
    
#     "/home/jovyan/cristian/outputs/drd2_0.7_clint_0.3_div_ScaffoldSimiliarty_V2P",
#     "/home/jovyan/cristian/outputs/drd2_0.7_clint_0.3_div_ScaffoldSimiliarty_V2P_#2",
#     "/home/jovyan/cristian/outputs/drd2_0.7_clint_0.3_div_ScaffoldSimiliarty_V2P_#3",
    
#     "/home/jovyan/cristian/outputs/drd2_0.6_fabs_0.1_fdiss_0.1_clint_0.1_vss_0.1_V2P",
#     "/home/jovyan/cristian/outputs/drd2_0.6_fabs_0.1_fdiss_0.1_clint_0.1_vss_0.1_V2P_#2",
#     "/home/jovyan/cristian/outputs/drd2_0.6_fabs_0.1_fdiss_0.1_clint_0.1_vss_0.1_V2P_#3"
# ]

experiments=[
    #"/home/jovyan/cristian/outputs/drd2_0.7_F_0.3_#3__div_ScaffoldSimilarity_v2p_#2",
    "/home/jovyan/cristian/outputs/drd2_0.7_F_0.3_#3__div_ScaffoldSimilarity_v2p_#3",
    "/home/jovyan/cristian/outputs/drd2_0.7_F_0.3_#3__div_ScaffoldSimilarity_v2p_#4"
]



models = ["fabs", "fdiss", "clint", "vss"]
columns = ["SMILES", "Score", "fabs", "fdiss", "clint", "vss", "drd2", "fabs (raw)", "fdiss (raw)", "clint (raw)", "vss (raw)", "drd2 (raw)"]
results_df = pd.DataFrame(columns=['Experiment', 'fabs', 'fdiss', 'clint', 'vss', 'drd2'])
BATCH_SIZE = 1000


for experiment in experiments:
    
    df = pd.read_csv(f"{experiment}/staged_learning_1.csv")
    existing_columns = [col for col in columns if col in df.columns]
    selected_data = df[existing_columns]
    smiles_non_zero = selected_data[selected_data["Score"] != 0]
    
    sampled_smiles = smiles_non_zero.sample(n=50000, random_state=42)
    sampled_smiles_list = sampled_smiles["SMILES"].tolist()
    

    print(experiment.split("/")[-1], len(smiles_non_zero))

    experiment_results = {}

    for model in models:
        #experiment_results[model] = df[f"{model} (raw)"].mean()
        print(model)        
        model_results = []
            
        for index in range(0, len(sampled_smiles_list), BATCH_SIZE):
            smi = sampled_smiles_list[index : index + BATCH_SIZE]
            input = "\n".join(smi)
            result = run_subprocess(model, input)
            data = json.loads(result.stdout)   
            model_results.extend(data["payload"]["predictions"])   
        print(len(model_results))
        mean_for_model = np.mean(model_results)
        experiment_results[model] = mean_for_model

    print(experiment_results)

    new_row = {'Experiment':experiment.split("/")[-1],
               'fabs': experiment_results["fabs"],
               'fdiss': experiment_results["fdiss"],
               'clint': experiment_results["clint"],
               'vss': experiment_results["vss"]}
    
    results_df = results_df.append(new_row, ignore_index=True)
    print(results_df)

results_df.to_csv('average_scores_oracles_F.csv', index=False)
        


    
    
    
    


