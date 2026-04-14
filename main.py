from src.pipelines.DataIngestionPipeline import DataIngestionPipeline
from src.pipelines.DataValidationPipeline import DataValidationPipeline
from src.pipelines.DataTransformPipeline import DataTransformPipeline
from src.pipelines.TrainingPipeline import TrainingPipeline

from src.utils.common import * 

if __name__=="__main__":
    logger.info("------------------- STAGE: DATA INGESTION STARTED ------------------- ")
    obj1=DataIngestionPipeline()
    ingested_data=obj1.start_ingestion()
    logger.info("------------------- STAGE: DATA INGESTION COMPLETED -------------------")
    if ingested_data is not None:
        logger.info("------------------- STAGE: DATA VALIDATION STARTED ------------------- ")
        obj2=DataValidationPipeline()
        status=obj2.start_validation(ingested_data)
        logger.info("------------------- STAGE: DATA VALIDATION COMPLETED -------------------")
        if status==True:
            logger.info("------------------- STAGE: DATA TRANSFORMATION STARTED ------------------- ")
            obj3=DataTransformPipeline()
            train_data,test_data=obj3.start_transformation(ingested_data)
            logger.info("------------------- STAGE: DATA TRANSFORMATION COMPLETED -------------------")
            logger.info("------------------- STAGE: MODEL TRAINING STARTED ------------------- ")
            obj4=TrainingPipeline(train_data,test_data)
            model=obj4.start_training_and_testing()
            logger.info("------------------- STAGE: MODEL TRAINING COMPLETED -------------------")

        else:
            raise Exception("Invalid Data - Please check the data")
    else:
        raise Exception("Invalid Data - Please check the filepath")
