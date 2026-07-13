from src.components.DataIngestion import DataIngestion
from src.utils.common import * 
import pandas as pd 
from ensure import ensure_annotations

class DataIngestionPipeline:
    def __init__(self):
        self.ingestion_obj=DataIngestion()
    
    @ensure_annotations
    def start_ingestion(self)->pd.DataFrame|None:
        logger.info("------------------- STAGE: DATA INGESTION STARTED ------------------- ")
        data=self.ingestion_obj.load_data()
        logger.info("------------------- STAGE: DATA INGESTION COMPLETED ------------------- ")
        return data
