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
            save_json(Path(VALIDATION_STATUS_FILE),{'Validation Status':VALIDATION_STATUS})
            return VALIDATION_STATUS
                    
    @ensure_annotations
    def clean_data(self,data:pd.DataFrame,validation_status:bool=False)->pd.DataFrame|None:
        if validation_status:
            data.drop_duplicates(inplace=True)
            data.fillna('Not Present',inplace=True)
            VALIDATED_DATA_PATH=os.path.join(self.VALIDATION_CONFIG.artifacts,self.VALIDATION_CONFIG.validated_filename)
            create_dirs(Path(self.VALIDATION_CONFIG.artifacts))
            data.to_csv(VALIDATED_DATA_PATH,index=False)
            logger.info(f"Cleaned and stored data successfully in {VALIDATED_DATA_PATH}")
            return data
        else:
            logger.fatal("Invalid data - Please check filepaths and data")
            return None
