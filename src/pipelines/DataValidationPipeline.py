from src.components.DataValidation import DataValidation 
from src.utils.common import * 
import pandas as pd
from ensure import ensure_annotations

class DataValidationPipeline:
    def __init__(self):
        logger.info("Data Validation pipeline initiated")
        self.obj=DataValidation()

    @ensure_annotations
    def start_validation(self,data:pd.DataFrame)->bool:
        VALIDATION_STATUS=self.obj.validate_data(data)
        return VALIDATION_STATUS