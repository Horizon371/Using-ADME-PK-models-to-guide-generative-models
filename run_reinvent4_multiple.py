import subprocess, optuna, logging, sys, statistics, time
import numpy as np
import pandas as pd


from ReinventAndromedaProject.config.create_config import ConfigBuilder

REINVENT = "/home/jovyan/cristian/REINVENT4/reinvent/Reinvent.py"
andromeda_models = ["fabs", "fdiss", "clint", "vss"]
td_commons_models = ["drd2", "jnk3"]

def run_reinvent():
    for i in range (5,6):
        config_builder = ConfigBuilder(f"_#3__div_ScaffoldSimilarity_v2p_#{i}")
                
        config_builder.set_batch_size(550)
        config_builder.set_max_steps(600)
                
        config_builder.add_scoring_component("drd2", weight=0.7) 
        config_builder.add_scoring_component("F", weight=0.3, confidence=0.7)
        # config_builder.add_scoring_component("fabs", weight=0.2, confidence=0.7) 
        # config_builder.add_scoring_component("fdiss", weight=0.2, confidence=0.7) 
        # config_builder.add_scoring_component("clint", weight=0.2, confidence=0.7) 
        # config_builder.add_scoring_component("vss", weight=0.2, confidence=0.7) 

        config = config_builder.build_config()
        run_reinvent_subprocess(config.logging_path, config.path, config.output_path)
                
        try:
            generate_statistics(config.output_path)
        except Exception as e:
            print(e)
        
def generate_statistics(output_folder):
    subprocess.run(["python3", "scripts/ReinventAndromedaProject/utils/compute_statistics.py", output_folder])

def objective(trial):
    weights = trial.suggest_float('x', 0.0, 1.0)
    print(weights)

    config_builder = ConfigBuilder(no_save = True)
          
    config_builder.set_batch_size(100)
    config_builder.set_max_steps(100)
    
    config_builder.add_scoring_component("drd2", weight=1)    
 
    config = config_builder.build_config()
    
    score = run_reinvent_subprocess(config.logging_path, config.path)
    return score


def objective_all(trial):
    n = 4
    models = ["fabs", "fdiss", "clint", "vss"]
    suggestions = []
    for i in range(n):
        suggestions.append(trial.suggest_float(models[i], 0.01, 1))
            
    p = []
    total = sum(suggestions)
    for i in range(n):
        value = round( (suggestions[i] / total) * 0.5, 1)
        p.append(value)

    for i in range(n):
        trial.set_user_attr(models[i], p[i])

    print(0.5, p)

    config_builder = ConfigBuilder(no_save = True) 
    
    config_builder.add_scoring_component("drd2", 0.5)    
    config_builder.add_scoring_component("fabs", float(p[0]), confidence=0.7)    
    config_builder.add_scoring_component("fdiss", float(p[1]), confidence=0.7)    
    config_builder.add_scoring_component("clint", float(p[2]), confidence=0.7)    
    config_builder.add_scoring_component("vss", float(p[3]), confidence=0.7)    
    
    config_builder.set_batch_size(100)
    config_builder.set_max_steps(100)
    
    config = config_builder.build_config()
    
    score = run_reinvent_subprocess(config.logging_path, config.path, config.output_path)
    return score
    
def run_reinvent_subprocess(logging_path, config_path, output_path):
    subprocess.run(["python3", REINVENT, "-l", logging_path, config_path])
    score = parse_generated_smiles_for_average_drd2_score(output_path)
    return score

#def parse_reinvent_logs_for_average_score(logging_path):
#    results = get_results(logging_path, "<INFO> Score")
#    return statistics.mean(results)

def parse_generated_smiles_for_average_drd2_score(output_path):
    generated = pd.read_csv(output_path + "/staged_learning_1.csv", usecols=["drd2"])
    return generated["drd2"].mean()

def get_results(file_path, substring):
    scores = []
    with open(file_path, 'r') as file:
        for line in file:
            if substring in line:
                scores.append(float(line.strip().split(" ")[3]))
    return scores

def run_optuna():
    optuna.logging.get_logger("optuna").addHandler(logging.StreamHandler(sys.stdout))
    study = optuna.create_study(direction="maximize")
    study.optimize(objective_all, n_trials=100)
    study_trials_df = study.trials_dataframe()
    study_trials_df.to_csv('study_trials_weights_drd2_fixed.csv', index=False)
    print(study.best_params)

run_reinvent()