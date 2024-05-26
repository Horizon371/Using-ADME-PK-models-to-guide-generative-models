import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


GENERATED_SMILES_CSV_NAME = "staged_learning_1.csv"
HISTOGRAM_SUBFOLDER = "score_histograms"
FOLDER_PATH = "/home/jovyan/cristian/outputs/drd2_0.7_clint_0.3_div_ScaffoldSimiliarty_V2P"

def generate_score_histograms(results_folder, steps = None):
    rows = 2
    columns = 4
    
    number_of_steps = rows * columns
    generated_smiles_csv = f"{results_folder}/{GENERATED_SMILES_CSV_NAME}"
    df = pd.read_csv(generated_smiles_csv)
    
    if not steps:
        steps = create_steps_list(df, number_of_steps)
    elif number_of_steps != len(steps):
        raise Exception(f"Size of the steps list ( {len(steps)} ) does not coincide with the one expected based on the number of rows and columns ( {number_of_steps} )")
    
    plot_figure(df, results_folder, rows, columns, steps)

def create_steps_list(df, number_of_steps):
    last_row_value = df.iloc[-1]["step"]
    steps = np.linspace(1, last_row_value, number_of_steps).astype(int)
    return steps

def plot_figure(df, results_folder, rows, columns, steps):
    fig, axs = plt.subplots(rows, columns, figsize=(6*columns, 6*rows)) 
    add_histograms_to_figure(df, steps, rows, columns, axs)
    set_figure_title_and_labels(fig, results_folder)    
    save_figure(results_folder)
    plt.clf()    

def add_histograms_to_figure(df, steps, rows, columns, axs):
    step_index = 0
    for row in range(rows):
        for column in range(columns):
            step = steps[step_index]
            step_df = df[df['step'] == step]
            plot_histogram(step_df, step, axs[row][column])
            step_index += 1
    
def plot_histogram(df, step, axs):
    scores_gt_zero = df[df['Score'] > 0]
    sns.histplot(scores_gt_zero['Score'], ax=axs, kde=False, bins=20, color='skyblue')
    axs.set_title(str(step), fontsize=18)
    axs.tick_params(labelsize=16)
    axs.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])  # Adjust the ticks as per your requirement
    axs.set_xlabel('')
    axs.set_ylabel('')

def set_figure_title_and_labels(fig, results_folder):
    title = results_folder.split("/")[-1]
    #fig.suptitle(title, fontsize=18)
    fig.text(0.5, 0.03, 'Score', ha='center', fontsize=22)
    fig.text(0.01, 0.5, 'Counts', va='center', rotation='vertical', fontsize=22)
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)

def save_figure(results_folder):
    histogram_save_path = f"{results_folder}/{HISTOGRAM_SUBFOLDER}"
    if not os.path.exists(histogram_save_path): 
        os.makedirs(histogram_save_path)
    
    last_subfolder = results_folder.split('/')[-1]

    plt.savefig(f'{histogram_save_path}/scores_{last_subfolder}.png')

def generate_histogram_for_step(target_step, results_folder):
    
    genrated_smiles_csv = f"{results_folder}/{GENERATED_SMILES_CSV_NAME}"
    
    df = pd.read_csv(genrated_smiles_csv)
    step_df = df[df['step'] == target_step]
    scores_gt_zero = step_df[step_df['Score'] > 0] # smiles with score greater than 0

    # Plot scores larger than 0 then add bars for scores=0 and invalid smiles
    sns.histplot(scores_gt_zero['Score'], kde=False, bins=20, color='skyblue')

    
    histogram_save_path = f"{results_folder}/{HISTOGRAM_SUBFOLDER}"
    
    if not os.path.exists(histogram_save_path): 
        os.makedirs(histogram_save_path)
    
    plt.savefig(f'{histogram_save_path}/step_{target_step}.png')
        
    
generate_score_histograms(FOLDER_PATH, [1, 20, 100, 150, 200, 250, 300, 330])