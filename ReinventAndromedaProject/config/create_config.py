import toml, os, shutil

BASE_CONFIG = "/home/jovyan/cristian/scripts/ReinventAndromedaProject/config/reinvent_config.toml"
DEFAULT_SIGMA = 128
DEFAULT_RATE = 0.0001
DEFAULT_BATCH_SIZE = 550
DEFAULT_MAX_STEPS = 600


class ConfigBuilder():
    
    def __init__(self, folder_suffix=None, no_save = False):
        '''
        We build the config starting from a base config file
        '''
        self.config = toml.load(BASE_CONFIG)
        self.config["stage"][0]["scoring"]["component"] = []
        self.components_list = self.config["stage"][0]["scoring"]["component"]
        self._folder_suffix = folder_suffix
        self._no_save = no_save
        self._sigma = DEFAULT_SIGMA
        self._rate = DEFAULT_RATE
        self._batch_size = DEFAULT_BATCH_SIZE
        self._max_steps = DEFAULT_MAX_STEPS
        self.models = []
        
    def set_sigma(self, sigma):
        self._sigma = sigma
        
    def set_rate(self, rate):
        self._rate = rate
        
    def set_batch_size(self, batch_size):
        self._batch_size = batch_size
    
    def set_max_steps(self, max_steps):
        self._max_steps = max_steps
        
    def add_scoring_component(self, model, weight, confidence = None):
        if weight > 0:
            arguments = self._make_arguments(model, confidence)
            component = self._create_scoring_component(model, arguments, weight)
            self.components_list.append(component)
            self.models.append(model)
            self.models.append(str(weight))
        
    def _make_arguments(self, model, confidence):
        args = f"/home/jovyan/cristian/scripts/ReinventAndromedaProject/run_andromeda.py {model}" 
        if confidence:
            args += f" confidence {confidence}"
        return args

    def _create_scoring_component(self, model, args, weight):
        component = { "external-process" : 
            {'endpoint': 
                [{
                  'name': f'{model}', 
                  'weight': weight, 
                  'params': {
                      'executable': '/home/jovyan/miniconda3/envs/reinvent4/bin/python', 
                      'args': args 
                    }
                }]
            }
        }
        return component

    def build_config(self): 
        folder_name = self._get_output_folder_name()
        output_path = self._create_output_path(folder_name)
        config_path = f"{output_path}/{folder_name}_config.toml"
        logging_path = f"{output_path}/{folder_name}_run.log"  
        self._update_config(output_path)
        return Config(self.config, config_path, logging_path, output_path)
    
    def _get_output_folder_name(self):
        if self._no_save:
            return "z_default"
        else:
            return self._build_output_folder_name()
    
    def _build_output_folder_name(self):
        output_folder = '_'.join(self.models)
        if self._folder_suffix:
            output_folder += self._folder_suffix
        return output_folder

    def _create_output_path(self, folder_name):
        output_folder = f"/home/jovyan/cristian/outputs/{folder_name}"
        if os.path.exists(output_folder): 
            shutil.rmtree(output_folder)
        os.makedirs(output_folder)
        return output_folder 

    def _update_config(self, output_path):
        self._update_config_output_paths(output_path)
        self._update_learning_strategy()
        self._update_stage_params()

    def _update_config_output_paths(self, output_path):
        self.config["tb_logdir"] = f"{output_path}/tb_logs"
        self.config["json_out_config"] = f"{output_path}/_staged_learning.json"
        self.config["parameters"]["summary_csv_prefix"] =  f"{output_path}/staged_learning"
        self.config["stage"][0]["chkpt_file"] = f"{output_path}/andromeda_reinvent.chkpt"
      
    def _update_learning_strategy(self):
        self.config["learning_strategy"]["sigma"] =  self._sigma
        self.config["learning_strategy"]["rate"] =  self._rate

    def _update_stage_params(self):
        self.config["stage"][0]["max_steps"] = self._max_steps
        self.config["parameters"]["batch_size"] = self._batch_size
        
class Config():
    def __init__(self, config, config_path, logging_path, output_path):
        self.config = config
        self.path = config_path
        self.logging_path = logging_path
        self.output_path = output_path
        with open(self.path, 'w') as file:
            toml.dump(self.config, file)
    