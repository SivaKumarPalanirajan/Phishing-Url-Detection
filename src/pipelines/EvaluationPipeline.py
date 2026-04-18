from src.utils.common import * 
from src.components.Evaluation import ModelEvaluation

class EvaluationPipeline:
    def __init__(self):
        self.obj1=ModelEvaluation()
        logger.info("Initialized Evaluation Pipeline")
    
    def start_evaluation(self,model,val_data:pd.DataFrame|None)->None:    
        logger.info("Started Evaluation")
        self.obj1.evaluate_on_val_data(model,val_data)