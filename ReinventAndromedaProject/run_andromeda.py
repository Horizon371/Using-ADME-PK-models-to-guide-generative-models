import sys
import json
from andromeda_model_resolver import AndromedaModelResolver, ModelOptionsResolver


def get_smiles_from_input():
    input = sys.stdin.read()
    smiles_list = input.split('\n')
    return smiles_list

def parse_arguments_for_model_name_and_options():
    arguments = sys.argv
    model_name = arguments[1]
    model_options = get_model_options(arguments)
    return model_name, model_options

def get_model_options(arguments):
    options_list = parse_arguments_for_options(arguments)
    options = []
    for option in options_list:
        option_type = ModelOptionsResolver.resolve(option[0])
        options.append(option_type)
        options.append(option[1])
    return options

def parse_arguments_for_options(arguments):
    if len(arguments) > 2:
        extra_arguments = arguments[2:]
        model_options = [extra_arguments[i:i+2] for i in range(0, len(extra_arguments), 2)]
        return model_options
    else:
        return []

def create_json_response(predicted_values: list):
    response = {}
    response["version"] = 1
    response["payload"] = {}
    response["payload"]["predictions"] = predicted_values
    return json.dumps(response)
    
smiles_list = get_smiles_from_input()
model_name, model_options = parse_arguments_for_model_name_and_options()
model = AndromedaModelResolver.resolve(model_name, model_options)
predictions = model.predict(smiles_list)
response_json = create_json_response(predictions)

# print response for REINVENT
print(response_json)


    