import sys
from compute_diversity import compute_and_plot_pairwise_similarities
from generate_histogram import generate_score_histograms
from compute_rediscovery import compute_rediscovery


SMI_FILE = "/home/jovyan/cristian/smiles/sanitizied_smiles_drd2.smi"


generated_smiles_folder = sys.argv[1]

print("\nGenerating score histograms for steps...")
generate_score_histograms(generated_smiles_folder)

print("\nComputing rediscovery...")
compute_rediscovery(SMI_FILE, generated_smiles_folder)

#print("\nComputing pairwise similarity of the generated compounds...")
#compute_and_plot_pairwise_similarities(generated_smiles_folder)

print("\nDone\n")