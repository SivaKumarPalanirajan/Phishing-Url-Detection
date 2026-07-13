from src.components.DataValidation import DataValidation 
from src.utils.common import * 
import pandas as pd
from ensure import ensure_annotations

class DataValidationPipeline:
    def __init__(self):
        self.obj=DataValidation()

    @ensure_annotations
    def start_validation(self,data:pd.DataFrame)->bool:
        logger.info("------------------- STAGE: DATA VALIDATION STARTED ------------------- ")
        VALIDATION_STATUS=self.obj.validate_data(data)
        logger.info("------------------- STAGE: DATA VALIDATION COMPLETED -------------------")
        return VALIDATION_STATUS