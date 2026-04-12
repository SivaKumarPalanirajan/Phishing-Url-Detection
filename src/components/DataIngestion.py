from src.utils.common import *
import pandas as pd 
from src.constants import CONFIG_PATH
import os 
from ensure import ensure_annotations

class DataIngestion:
    def __init__(self):
        CONFIG_DATA=load_yaml(CONFIG_PATH)
        self.INGESTION_CONFIG=CONFIG_DATA.data_ingestion
        logger.info("Loaded Ingestion pipeline Configuration data")
    
    @ensure_annotations
    def load_data(self)->pd.DataFrame|None:
        dir=self.INGESTION_CONFIG.artifacts
        filename=self.INGESTION_CONFIG.filename
        DATA_PATH=os.path.join(dir,filename)
        if os.path.exists(DATA_PATH):
            dir,ext=os.path.splitext(DATA_PATH)
            if ext=='.xlsx':
                self.data=pd.read_excel(DATA_PATH)
            elif ext=='.csv':
                self.data=pd.read_csv(DATA_PATH)
            else:
                logger.error("Invalid Filename - File Extension isn't an excel or csv")
                self.data=None
                return self.data
            logger.info("Loaded data successfully")
            return self.data
        else:
            logger.error("Invalid filepath")
            return None

