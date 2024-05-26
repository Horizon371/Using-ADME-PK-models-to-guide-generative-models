from andromeda_wrappers.models import *

class AndromedaModelResolver:
    """
    Resolver that picks the right model
    """
    
    def __init__(self, name):
        self.name = name
        
    def resolve(name, options):
        if name == "fabs":
            return FabsModel(options)
        elif name == "fdiss":
            return FdissModel(options)
        elif name == "clint":
            return CLint(options)
        elif name == "vss":
            return Vss(options)
        elif name == "F":
            return BioavailabilityModel(options)
        elif name == "halflife":
            return HalfLifeModel(options)
        elif name == "drd2":
            return Drd2BindingSiteModel()
        elif name == "jnk3":
            return Jnk3BindingSiteModel()
        else:
            raise Exception(f" < {name} > is an invalid ANDROMEDA model name")
            
            
class ModelOptionsResolver:
    
    @staticmethod
    def resolve(option: str):
        if option == "confidence":
            return ModelOptions.CONFIDENCE
        else:
            raise Exception("{option} is an invalid ANDROMEDA model option")


class ModelOptions:
    CONFIDENCE = "--confidences"

        
        
