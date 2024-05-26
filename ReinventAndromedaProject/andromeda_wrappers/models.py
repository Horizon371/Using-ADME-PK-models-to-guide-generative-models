from andromeda_wrappers.base_andromeda_model_wrapper import ModelPath, AndromedaRegressionModel, BasePredictiveModel, BioavailabilityModel, HalfLifeModel
from tdc import Oracle

class FabsModel(AndromedaRegressionModel):
    
    def __init__(self, options):
        super().__init__(ModelPath.FABS, 0.6, 1, options)
        
    def _score(self, prediction: list):
        return self._score_fraction(prediction)


class FdissModel(AndromedaRegressionModel):
    
    def __init__(self, options):
        super().__init__(ModelPath.FDISS, 0.95, 1, options)
        
    def _score(self, prediction: list):
        return self._score_fraction(prediction)
    
    
class CLint(AndromedaRegressionModel):
    
    def __init__(self, options):
        super().__init__(ModelPath.CLINT, 2, 4, options)
        
    def _score(self, prediction: list):
        return self._score_interval(prediction)
        
        
class Vss(AndromedaRegressionModel):
    
    def __init__(self, options):
        super().__init__(ModelPath.VSS, -1, 1, options)
        
    def _score(self, prediction: list):
        return self._score_interval(prediction)
        
    
class Drd2BindingSiteModel(BasePredictiveModel):
            
    def predict(self, smiles_list):
        oracle = Oracle(name = 'DRD2')
        return oracle(smiles_list)

class Jnk3BindingSiteModel(BasePredictiveModel):
            
    def predict(self, smiles_list):
        oracle = Oracle(name = 'JNK3')
        return oracle(smiles_list)
        
