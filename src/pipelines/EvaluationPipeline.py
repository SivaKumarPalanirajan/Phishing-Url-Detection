from src.utils.common import * 
from src.components.Evaluation import ModelEvaluation
from src.constants import CONFIG_PATH 
import pandas as pd 

class EvaluationPipeline:
    def __init__(self,model=None,val_data:pd.DataFrame|None=None):
        self.obj1=ModelEvaluation()
        EVALUATION_CONFIG=load_yaml(CONFIG_PATH).model_evaluation
        if model is None:
            MODEL_PATH=os.path.join(EVALUATION_CONFIG.artifacts_training,EVALUATION_CONFIG.model_filename)
            model=load_model(MODEL_PATH)
        if val_data is None:
            VAL_DATA_PATH=os.path.join(EVALUATION_CONFIG.artifacts_transformation,EVALUATION_CONFIG.val_data_filename)
            val_data=pd.read_csv(VAL_DATA_PATH)

        self.model=model 
        self.val_data=val_data

    def start_evaluation(self):    
        logger.info("------------------- STAGE: MODEL EVALUATION STARTED ------------------- ")
        self.obj1.evaluate_on_val_data(self.model,self.val_data)
        logger.info("------------------- STAGE: MODEL EVALUATION COMPLETED -------------------")

if __name__=='__main__':
    obj1=EvaluationPipeline()
    obj1.start_evaluation()
