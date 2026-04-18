import pandas as pd 
from src.utils.common import *
from src.constants import CONFIG_PATH,SCHEMA_PATH
import mlflow 
from sklearn.metrics import accuracy_score,precision_score,recall_score,classification_report

class ModelEvaluation:
    def __init__(self):
        self.TRAIN_CONFIG=load_yaml(CONFIG_PATH).model_training
        self.EVAL_CONFIG=load_yaml(CONFIG_PATH).model_evaluation
        self.TRANSFORM_CONFIG=load_yaml(CONFIG_PATH).data_transformation
        self.SCHEMA=load_yaml(SCHEMA_PATH)
        self.useful_features=self.TRAIN_CONFIG.useful_features

        create_dirs(self.EVAL_CONFIG.artifacts)

    
    def evaluate_on_val_data(self,model,val_data:pd.DataFrame|None)->None:
        if val_data is None:
            val_data_path=os.path.join(self.TRANSFORM_CONFIG.artifacts,self.TRANSFORM_CONFIG.val_data_filename)
            val_data=pd.read_csv(val_data_path)

        if model is None:
            model_path=os.path.join(self.TRAIN_CONFIG.artifacts,self.TRAIN_CONFIG.model_filename)
            self.model=load_model(model_path)
        else:
            self.model=model
            
        model_version_path=os.path.join(self.TRAIN_CONFIG.artifacts,self.TRAIN_CONFIG.model_version_filename)
        self.model_version=load_json(model_version_path).version
        logger.info(f'Loaded model {self.model_version}')

        logger.info(f'Loaded validation data')
        inp_cols=[col for col,_ in self.SCHEMA.INP_COLS.items()]
        tar_col=[col for col,_ in self.SCHEMA.TARGET_COL.items()]

        x_val=val_data[self.useful_features]
        y_val=val_data[tar_col]

        mlflow.set_experiment("Phising-Url-Detection")
        with mlflow.start_run(run_name=f"Evaluation - v{self.model_version}"):
            y_pred=self.model.predict(x_val)
            accuracy=accuracy_score(y_val,y_pred)
            precision=precision_score(y_val,y_pred)
            recall=recall_score(y_val,y_pred)
            classif_report=classification_report(y_val,y_pred,target_names=['Not Phishing','Phishing'])
            logger.info(f"Accuracy: {accuracy}")
            logger.info(f"Precision: {precision}")
            logger.info(f"Recall: {recall}")
            logger.info(f"Classification: \n {classif_report}")
            metrics_json={'Accuracy':accuracy,"Precision":precision,"Recall":recall}
            mlflow.log_metrics(metrics_json)
            mlflow.log_text(str(classif_report),'ClassificationReport.txt')

        metrics_json_path=os.path.join(self.EVAL_CONFIG.artifacts,self.EVAL_CONFIG.metrics_filename)
        save_json(metrics_json_path,metrics_json)


