from src.components.DataTransform import DataTransform
from src.utils.common import * 
import pandas as pd 
from ensure import ensure_annotations
from src.pipelines.DataIngestionPipeline import DataIngestionPipeline 
from src.pipelines.DataValidationPipeline import DataValidationPipeline

class DataTransformPipeline:
    def __init__(self):
        self.obj=DataTransform()
    
    @ensure_annotations
    def start_transformation(self,data:pd.DataFrame)->tuple:
        logger.info("------------------- STAGE: DATA TRANSFORMATION STARTED ------------------- ")
        preprocessed_data=self.obj.preprocess_data(data)
        train,test,val=self.obj.training_testing_data_creation(preprocessed_data)
        logger.info("------------------- STAGE: DATA TRANSFORMATION COMPLETED ------------------- ")
        return train,test,val

if __name__=='__main__':
    obj1=DataIngestionPipeline()
    data=obj1.start_ingestion()
    if data is not None:
        obj2=DataValidationPipeline()
        status=obj2.start_validation(data)
        if status:
            obj3=DataTransformPipeline()
            train_data,test_data,val_data=obj3.start_transformation(data)
        else:
            raise Exception("Invalid Data - Please check the data")
    else:
        raise Exception("Invalid Data - Please check the filepath")
