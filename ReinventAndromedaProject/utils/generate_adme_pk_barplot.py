import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



computed_averages_path = "/home/jovyan/cristian/average_scores_oracles_50000.csv"

oracles = ['fabs', 'fdiss', 'vss', 'clint']
special_oracles = [r'$f_{abs}$', r'$f_{diss}$',  r'$V_{ss}$', r'$CL_{int}$']
categories = ["DRD2", r'+$f_{abs}$', r'+$f_{diss}$',  r'+$V_{ss}$', r'+$CL_{int}$', "+all", "+F"]
colors = [ 'steelblue','tan','lightseagreen', 'salmon','peru', 'violet']
   
def create_average_and_std(experiment_measurements):
    avg = sum(experiment_measurements) / 3 
    std = np.std(experiment_measurements) / np.sqrt(3)
    return avg, std
    
def compute_averages_and_std(property_measurements):
    averages = []
    standard_deviations = []
    
    for measurement_index in range(0, len(property_measurements), 3):
        experiment_measurements = property_measurements[measurement_index : measurement_index + 3]
        print(experiment_measurements)
        avg, std = create_average_and_std(experiment_measurements)
        averages.append(avg)
        standard_deviations.append(std)
        
    return averages, standard_deviations


def plot_barplot():
    num_groups = len(oracles)
    num_categories = len(categories)

    bar_width = 0.18

    r1 = np.arange(num_categories)
    positions = [r1 + i * bar_width for i in range(num_groups)]

    fig, ax = plt.subplots(figsize=(12, 6))

    for i in range(num_groups):
        bars = ax.bar(positions[i], average_properties[i], width=bar_width, color=colors[i], yerr=errors[i], capsize=0, label=special_oracles[i])
        for bar, error in zip(bars, errors[i]):
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval + error + 0.01, round(yval, 2), ha='center', va='bottom')        
    # bars = ax.bar(categories, average_properties)

    # for bar in bars:
    #     height = bar.get_height()
    #     ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1, str(height), ha='center', fontsize='large')


    plt.xlabel('RL Agents', fontsize=13)
    plt.ylabel('Average property values',  fontsize=13)
    ax.set_xticks([r + bar_width * (num_groups - 1) / 2 for r in range(num_categories)])
    ax.set_xticklabels(categories)
    plt.tick_params(axis='both', which='major', labelsize=13)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='large')
    plt.subplots_adjust(left = 0.06, right=0.9, top = 0.95)  # Adjust the right side to make room for the legend
    plt.savefig("grouped_barplot")
    plt.show()




experiments = pd.read_csv(computed_averages_path)
average_properties = []
errors = []

for oracle in oracles:
    print(oracle)
    avg, std = compute_averages_and_std(experiments[oracle].tolist())
    average_properties.append(avg)
    errors.append(std)
print(average_properties)
plot_barplot()


