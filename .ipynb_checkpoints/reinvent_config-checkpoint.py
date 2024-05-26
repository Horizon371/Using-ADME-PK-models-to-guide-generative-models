import sys, os, json

output_dir = sys.argv[1]
config = sys.argv[2]


configuration = {
    "version": 3,                          
    "run_type": "reinforcement_learning",  # other run types: "sampling", "validation",
                                           #                  "transfer_learning",
                                           #                  "scoring" and "create_model",
    "model_type": "default"
}


# add the "parameters" block
configuration["parameters"] = {}


# add a "diversity_filter"
configuration["parameters"]["diversity_filter"] =  {
    "name": "IdenticalMurckoScaffold",     # other options are: "IdenticalTopologicalScaffold", 
                                           #                    "NoFilter" and "ScaffoldSimilarity"
                                           # -> use "NoFilter" to disable this feature
    "nbmax": 25,                           # the bin size; penalization will start once this is exceeded
    "minscore": 0.4,                       # the minimum total score to be considered for binning
    "minsimilarity": 0.4                   # the minimum similarity to be placed into the same bin
}


# prepare the inception (we do not use it in this example, so "smiles" is an empty list)
configuration["parameters"]["inception"] = {
    "smiles": [],                          # fill in a list of SMILES here that can be used (or leave empty)
    "memory_size": 100,                    # sets how many molecules are to be remembered
    "sample_size": 10                      # how many are to be sampled each epoch from the memory
}

# set all "reinforcement learning"-specific run parameters
configuration["parameters"]["reinforcement_learning"] = {
    "prior": "/home/jovyan/cristian/REINVENT4/priors/reinvent.prior", # path to the pre-trained model
    "agent": "/home/jovyan/cristian/REINVENT4/priors/reinvent.prior", # path to the pre-trained model
    "n_steps": 125,                        # the number of epochs (steps) to be performed; often 1000
    "sigma": 128,                          # used to calculate the "augmented likelihood", see publication
    "learning_rate": 0.0001,               # sets how strongly the agent is influenced by each epoch
    "batch_size": 128,                     # specifies how many molecules are generated per epoch
    "margin_threshold": 50                 # specify the (positive) margin between agent and prior
}


# prepare the scoring function definition and add at the end
scoring_function = {
    "name": "custom_product",              # this is our default one (alternative: "custom_sum")
    "parallel": False,                     # sets whether components are to be executed
                                           # in parallel; note, that python uses "False" / "True"
                                           # but the JSON "false" / "true"

    # the "parameters" list holds the individual components
    "parameters": [

    # add component: calculate the QED drug-likeness score (using RDkit)
    {
        "component_type": "qed_score",
        "name": "QED Score",                   # arbitrary name for the component
        "weight": 1,                           # the weight of the component (default: 1)
    }]
}




configuration["parameters"]["scoring_function"] = scoring_function

# write the configuration file to the disc
with open(config, 'w') as f:
    json.dump(configuration, f, indent=4, sort_keys=True)
