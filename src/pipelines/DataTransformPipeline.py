from src.components.DataTransform import DataTransform
from src.utils.common import * 
import pandas as pd 
from ensure import ensure_annotations

class DataTransformPipeline:
    def __init__(self):
        logger.info("Data transform pipeline initiated")
    
    @ensure_annotations
    def start_transformation(self,data:pd.DataFrame)->tuple:
        obj=DataTransform()
        preprocessed_data=obj.preprocess_data(data)
        train,test,val=obj.training_testing_data_creation(preprocessed_data)
        return train,test,val