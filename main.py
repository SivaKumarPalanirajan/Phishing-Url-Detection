from src.pipelines.DataIngestionPipeline import DataIngestionPipeline
from src.pipelines.DataValidationPipeline import DataValidationPipeline
from src.pipelines.DataTransformPipeline import DataTransformPipeline
from src.pipelines.TrainingPipeline import TrainingPipeline
from src.pipelines.EvaluationPipeline import EvaluationPipeline

from src.utils.common import * 

if __name__=="__main__":
    
    obj1=DataIngestionPipeline()
    ingested_data=obj1.start_ingestion()

    if ingested_data is not None:
        obj2=DataValidationPipeline()
        status=obj2.start_validation(ingested_data)
        if status==True:

            obj3=DataTransformPipeline()
            train_data,test_data,val_data=obj3.start_transformation(ingested_data)

            obj4=TrainingPipeline(train_data,test_data)
            model=obj4.start_training_and_testing()

            obj4=EvaluationPipeline(model,val_data)
            obj4.start_evaluation()
        else:
            raise Exception("Invalid Data - Please check the data")
    else:
        raise Exception("Invalid Data - Please check the filepath")
