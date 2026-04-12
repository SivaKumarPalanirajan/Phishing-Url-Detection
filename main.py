from src.pipelines.DataIngestionPipeline import DataIngestionPipeline
from src.pipelines.DataValidationPipeline import DataValidationPipeline
from src.pipelines.DataTransformPipeline import DataTransformPipeline

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
            train,test=obj3.start_transformation(ingested_data)
            logger.info("------------------- STAGE: DATA TRANSFORMATION COMPLETED -------------------")
        else:
            raise Exception("Invalid Data - Please check the data")
    else:
        raise Exception("Invalid Data - Please check the filepath")