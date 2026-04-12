from src.pipelines.DataIngestionPipeline import DataIngestionPipeline
from src.pipelines.DataValidationPipeline import DataValidationPipeline
from src.utils.common import * 

if __name__=="__main__":
    logger.info("STAGE: DATA INGESTION STARTED")
    obj1=DataIngestionPipeline()
    ingested_data=obj1.start_ingestion()
    logger.info("------------------- STAGE: DATA INGESTION COMPLETED -------------------")
    if ingested_data is not None:
        logger.info("STAGE: DATA VALIDATION STARTED")
        obj2=DataValidationPipeline()
        obj2.start_validation(ingested_data)
        logger.info("------------------- STAGE: DATA VALIDATION COMPLETED -------------------")
