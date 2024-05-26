import subprocess, json
from abc import ABC, abstractmethod
import cmath

JAVA = "/usr/bin/java"
CP_SIGN = "/home/jovyan/cristian/cpsign/cpsign-2.0.0-rc6-fatjar.jar"
MODEL = "/home/jovyan/cristian/scripts/ReinventAndromedaProject/ANDROMEDA/fabs.jar"
SMILES_CSV = "/home/jovyan/cristian/outputs/smiles.csv"
   
   
class BasePredictiveModel(ABC):
    
    @abstractmethod
    def predict(self, smiles_list):
        pass
          
   
class BaseAndromedaModelWrapper(BasePredictiveModel):
    """
    Base wrapper class for the ANDROMEDA models
    """
    
    def __init__(self, model_path, options = None):
        self.model_path = model_path
        self.options = options
        self.smiles_list = SMILES_CSV + "_".join(options)    
        
    def predict(self, smiles_list):
        self._create_smiles_csv(smiles_list, SMILES_CSV)
        subprocess = self._run_subprocess(SMILES_CSV)
        result = self._extract_result_from_output(subprocess)
        predictions = self._get_predictions(result)
        smiles_scores = self._compute_scores_for_predictions(predictions)
        return smiles_scores
       
    def _create_smiles_csv(self, smiles_list, smiles_csv):
        """
        The SMILES strings have to be passed to CPSign as a csv file
        """
        with open(smiles_csv, 'w', newline='') as f:
            f.write("SMILES" + '\n')
            for smiles in smiles_list:
                f.write(smiles + '\n') 
                
    def _run_subprocess(self, smiles_csv):
        command = self._build_command(smiles_csv)
        return subprocess.run(
            command,
            stdout=subprocess.PIPE, 
            text=True
        )
    
    def _build_command(self, smiles_csv):
        command = [JAVA, "-jar", CP_SIGN, "predict", "--model", self.model_path, "--predict-file", "csv", smiles_csv]
        if self.options:
            return command + self.options
        return command
            
    def _extract_result_from_output(self, process):
        output = process.stdout.replace("\n", "").replace("\t", "")
        selected_text = self._select_json_result(output)
        return json.loads(selected_text)

    def _select_json_result(self, output):
        left_bound = "Computing predictions... "
        right_bound = "Successfully predicted"
        start_index = output.find(left_bound) + len(left_bound)
        end_index = output.find(right_bound)
        return output[start_index:end_index]
     
    def _get_predictions(self, result):
        predictions = []
        for prediction in result:
            prediction_values = self._get_values_from_prediction(prediction)
            predictions.append(prediction_values)
        return predictions

    @abstractmethod                       
    def _get_values_from_prediction(self,prediction):
        pass
    
    def _compute_scores_for_predictions(self, predictions):
        scores = []
        for prediction in predictions:
            prediction_score = self._score(prediction)
            scores.append(prediction_score)
        return scores

    @abstractmethod
    def _score(self, prediction: list):
        pass
        
class AndromedaRegressionModel(BaseAndromedaModelWrapper):
    
    def __init__(self, model_path, optimum_lower, optimum_upper, options = None):
        super().__init__(model_path, options)          
        self.optimum_lower = optimum_lower
        self.optimum_upper = optimum_upper
                    
    def _get_values_from_prediction(self, prediction):
        midpoint = prediction["prediction"]["midpoint"]
        range_lower = prediction["prediction"]["intervals"][0]["rangeLowerCapped"]
        range_upper = prediction["prediction"]["intervals"][0]["rangeUpperCapped"]
        return [midpoint, range_lower, range_upper]
        
    def _get_overlap_percentage(self, computed_lower, computed_upper):
        predicted_interval_length = computed_upper - computed_lower
        overlap = max(0, min(computed_upper, self.optimum_upper) - max(computed_lower, self.optimum_lower))
        overlap_percentage = overlap / predicted_interval_length if predicted_interval_length > 0 else 0
        return overlap_percentage
        
    def _score_fraction(self, prediction):
        computed_lower = prediction[1]
        if computed_lower >= 1: return 1
            
        computed_upper = min(prediction[2], 1)
        overlap_percentage = self._get_overlap_percentage(computed_lower, computed_upper)           
        return overlap_percentage
        
    def _score_interval(self, prediction):
        computed_lower = prediction[1]
        computed_upper = prediction[2]
        overlap_percentage = self._get_overlap_percentage(computed_lower, computed_upper)           
        return overlap_percentage    
            
               
class AndromedaClassificationModel(BaseAndromedaModelWrapper):
        
    def __init__(self, model_path, options = None):
        super().__init__(model_path, options)          

    def _get_values_from_prediction(self, prediction):
        p_values = prediction["prediction"]["pValues"]
        return [p_values["1"], p_values["-1"]]     
        
        
class HalfLifeModel(BaseAndromedaModelWrapper):
    
    def __init__(self, options = None):
        super().__init__("", options)          
    
    def cap(self, output, model):
        if  model == "fu":
            if output > 4:
                return 4
            elif output < -2.7:
                return -2.7
            return output 
        
        elif model == "vss":
            if output < -1.3:
                return -1.3
            return output
        
        elif model == "clint":
            return output

        
    def convert(self, output, model):
        if model == "vss" or model =="clint":
            return 10**output
        elif model == "fu":
            return 1/(10**output + 1)
            
    def cap_and_convert(self, output, model):
        capped_output = self.cap(output, model)
        converted_output = self.convert(capped_output, model)
        return converted_output
    
    def predict(self, smiles_list):
        scores = []

        vss_scores = self._run_and_get_results(smiles_list, ModelPath.VSS)
        clint_scores = self._run_and_get_results(smiles_list, ModelPath.CLINT)
        fu_scores = self._run_and_get_results(smiles_list, ModelPath.FU)

        for vss_raw, clint_raw, fu_raw  in zip(vss_scores, clint_scores, fu_scores):
            
            fu = self.cap_and_convert(fu_raw, "fu")
            vss = self.cap_and_convert(vss_raw, "vss")
            clint = self.convert(clint_raw, "clint")
            
            half_life = self._compute_score_half_life(vss, clint, fu)     
            
           #scaled_scores = (scores - min_score) / (max_score - min_score)

            scores.append(half_life) 
            
        return scores

                
    
    def _compute_score_half_life(self, vss, clint, fu):
        clh = (clint * fu * 1500)/(clint * fu + 1500)
        cl = clh + 125 * fu
        cl = cl * 60 / 1000
        half_life = 0.69 * (vss*70) / cl
        return half_life


    def _run_subprocess(self, smiles_csv, model):
        command = self._build_command(smiles_csv, model)
        return subprocess.run(
            command,
            stdout=subprocess.PIPE, 
            text=True
        )
        
    def _get_values_from_prediction(self, prediction):
        midpoint = prediction["prediction"]["midpoint"]
        return midpoint
    
    def _build_command(self, smiles_csv, model):
        command = [JAVA, "-jar", CP_SIGN, "predict", "--model", model, "--predict-file", "csv", smiles_csv]
        if self.options:
            return command + self.options
        return command
    
    def _run_and_get_results(self, smiles_list, model):
        self._create_smiles_csv(smiles_list, SMILES_CSV)
        subprocess = self._run_subprocess(SMILES_CSV, model)
        result = self._extract_result_from_output(subprocess)
        predictions = self._get_predictions(result)
        return predictions
    
    def _score(self, prediction: list):
        pass
        
class BioavailabilityModel(BaseAndromedaModelWrapper):
    
    def __init__(self, options = None):
        super().__init__("", options)          
    
    def cap(self, output, model):
        if model == "fabs" or model == "fdiss":
            if output > 1:
                return 1
            elif output < 0:
                return 0
            return output 
        
        elif  model == "fu":
            if output > 4:
                return 4
            elif output < -2.7:
                return -2.7
            return output 
        
        elif model == "vss":
            if output < -1.3:
                return -1.3
            return output
        
        elif model == "clint":
            return output

        
    def convert(self, output, model):
        if model == "fabs" or model == "fdiss":
            return output
        elif model == "vss" or model =="clint":
            return 10**output
        elif model == "fu":
            return 1/(10**output + 1)
            
    def cap_and_convert(self, output, model):
        capped_output = self.cap(output, model)
        converted_output = self.convert(capped_output, model)
        return converted_output
    
    def predict(self, smiles_list):
        scores = []
        fabs_scores = self._run_and_get_results(smiles_list, ModelPath.FABS)
        fu_scores = self._run_and_get_results(smiles_list, ModelPath.FU)
        fdiss_scores = self._run_and_get_results(smiles_list, ModelPath.FDISS)
        clint_scores = self._run_and_get_results(smiles_list, ModelPath.CLINT)
    
        for fabs_raw, fu_raw, fdiss_raw, clint_raw in zip(fabs_scores, fu_scores, fdiss_scores, clint_scores):
            fabs = self.cap_and_convert(fabs_raw, "fabs")
            fu = self.cap_and_convert(fu_raw, "fu")
            fdiss = self.cap_and_convert(fdiss_raw, "fdiss")
            clint = self.convert(clint_raw, "clint")
            bioavailability = self._compute_score(fabs, fu, fdiss, clint)     
            scores.append(bioavailability) 
            
        return scores

                
    def _compute_score(self, fabs, fu, fdiss, clint):
        clh = (clint * fu * 1500)/(clint * fu + 1500)
        f = fabs * fdiss * ( 1 - clh/1500)
        
        if f > 1:
            return 1
        else:
            return f
    
    # def _compute_score_half_life(self, vss, clint, fu):
    #     clh = (clint * fu * 1500)/(clint * fu + 1500)
    #     cl = clh + 125 * fu
    #     cl = cl * 60 / 1000
    #     half_life = 0.69 * (vss*70) / cl
    #     return half_life


    def _run_subprocess(self, smiles_csv, model):
        command = self._build_command(smiles_csv, model)
        return subprocess.run(
            command,
            stdout=subprocess.PIPE, 
            text=True
        )
        
    def _get_values_from_prediction(self, prediction):
        midpoint = prediction["prediction"]["midpoint"]
        return midpoint
    
    def _build_command(self, smiles_csv, model):
        command = [JAVA, "-jar", CP_SIGN, "predict", "--model", model, "--predict-file", "csv", smiles_csv]
        if self.options:
            return command + self.options
        return command
    
    def _run_and_get_results(self, smiles_list, model):
        self._create_smiles_csv(smiles_list, SMILES_CSV)
        subprocess = self._run_subprocess(SMILES_CSV, model)
        result = self._extract_result_from_output(subprocess)
        predictions = self._get_predictions(result)
        return predictions
    
    def _score(self, prediction: list):
        pass
   
         
class ModelPath:
    FABS = "/home/jovyan/cristian/scripts/ReinventAndromedaProject/ANDROMEDA/fabs.jar"
    FDISS = "/home/jovyan/cristian/scripts/ReinventAndromedaProject/ANDROMEDA/fdiss.jar"
    VSS = "/home/jovyan/cristian/scripts/ReinventAndromedaProject/ANDROMEDA/Vss.jar"
    CLINT = "/home/jovyan/cristian/scripts/ReinventAndromedaProject/ANDROMEDA/CLint.jar"
    FU = "/home/jovyan/cristian/scripts/ReinventAndromedaProject/ANDROMEDA/fu.jar"