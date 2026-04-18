from src.components.Trainer import ModelTrainer
from src.utils.common import *
from src.constants import CONFIG_PATH,SCHEMA_PATH
from ensure import ensure_annotations

class TrainingPipeline:
    
    @ensure_annotations
    def __init__(self,TRAINING_DATA: pd.DataFrame | None = None ,TESTING_DATA: pd.DataFrame | None = None ):
        TRAINING_CONFIG=load_yaml(CONFIG_PATH).model_training
        self.training_data=TRAINING_DATA 
        self.testing_data=TESTING_DATA

        if self.training_data is None: 
            TRAINING_DATA_PATH=os.path.join(TRAINING_CONFIG.transformed_filepath,TRAINING_CONFIG.training_data_filename)
            self.training_data=pd.read_csv(TRAINING_DATA_PATH)
        if self.testing_data is None:
            TESTING_DATA_PATH=os.path.join(TRAINING_CONFIG.transformed_filepath,TRAINING_CONFIG.testing_data_filename)
            self.testing_data=pd.read_csv(TESTING_DATA_PATH)

        logger.info('Training pipeline has been initialized')

    def start_training_and_testing(self):
        obj=ModelTrainer(self.training_data,self.testing_data)
        model=obj.training()
        obj.testing()
        return model