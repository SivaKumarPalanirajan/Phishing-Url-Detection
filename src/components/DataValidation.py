from src.utils.common import * 
from src.constants import SCHEMA_PATH,CONFIG_PATH 
import pandas as pd 
from ensure import ensure_annotations

class DataValidation:
    def __init__(self):
        self.VALIDATION_CONFIG=load_yaml(CONFIG_PATH).data_validation

    @ensure_annotations
    def validate_data(self,data:pd.DataFrame)->bool:
        if data is not None:
            schema=load_yaml(SCHEMA_PATH) 
            inp_schema=schema.INP_COLS
            tar_schema=schema.TARGET_COL
            VALIDATION_STATUS = True
            for col,data_type in inp_schema.items():
                try:
                    if data[col].dtype==data_type:
                        continue 
                    else:
                        logger.info(f"Mismatch in {col} dtype")
                        VALIDATION_STATUS = False 
                except Exception as e:
                    logger.exception(f"Data validation failed - {e} ")
                    VALIDATION_STATUS = False
            if VALIDATION_STATUS==True:
                logger.info(f"Data validation is completed, proceeding with basic cleaning of data")
            create_dirs(Path(self.VALIDATION_CONFIG.artifacts))
            VALIDATION_STATUS_FILE=os.path.join(self.VALIDATION_CONFIG.artifacts,self.VALIDATION_CONFIG.validation_status_file)
            save_json(Path(VALIDATION_STATUS_FILE),{'validation_status':VALIDATION_STATUS})
            return VALIDATION_STATUS