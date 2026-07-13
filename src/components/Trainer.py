import pandas as pd 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import accuracy_score,classification_report
from src.constants import CONFIG_PATH,SCHEMA_PATH
from src.utils.common import *
import mlflow 
from mlflow.models import infer_signature 
import mlflow.sklearn  
import json 
from ensure import ensure_annotations
from scipy.sparse import hstack
from dotenv import load_dotenv

load_dotenv()
class ModelTrainer:

    @ensure_annotations
    def __init__(self,TRAINING_DATA: pd.DataFrame ,TESTING_DATA: pd.DataFrame):
        CONFIG=load_yaml(CONFIG_PATH)
        TRAINING_CONFIG=CONFIG.model_training
        self.TRANSFORM_CONFIG=CONFIG.data_transformation

        SCHEMA=load_yaml(SCHEMA_PATH)
        create_dirs(TRAINING_CONFIG.artifacts)

        self.inp_features=[col for col,_ in SCHEMA.INP_COLS.items()]
        self.target_feature=[col for col,_ in SCHEMA.TARGET_COL.items()][0]
        self.useful_features=TRAINING_CONFIG.useful_features

        self.training_data=TRAINING_DATA 
        self.testing_data=TESTING_DATA

        self.model_version_filepath = os.path.join(TRAINING_CONFIG.artifacts,TRAINING_CONFIG.model_version_filename)
        self.model=RandomForestClassifier(n_estimators=TRAINING_CONFIG.num_estimators,max_depth=TRAINING_CONFIG.max_depth)
        self.model_filepath=os.path.join(TRAINING_CONFIG.artifacts,TRAINING_CONFIG.model_filename)
        self.inf_model_filepath=os.path.join(TRAINING_CONFIG.artifacts_inferencing,TRAINING_CONFIG.model_filename)
        logger.info('Initialized RandomForest Classifier')

    def training(self):
        self.preprocessors={}

        y_train=self.training_data[self.target_feature]
        logger.info('Started training using the features: %s',self.useful_features)

        for col in self.useful_features:
            if col in ['url','tld','dom']:
                encoder=load_model(Path(os.path.join(self.TRANSFORM_CONFIG.artifacts,f"{self.TRANSFORM_CONFIG.encoder_filename}_{col}.pkl")))
                self.preprocessors[col]=encoder
            else:
                scaler=load_model(Path(os.path.join(self.TRANSFORM_CONFIG.artifacts,self.TRANSFORM_CONFIG.scaler_filename)))
                self.preprocessors['numerical']=scaler

        logger.info('Loaded preprocessing components')

        x_train_url_encoded=self.preprocessors['url'].transform(self.training_data['url'])
        x_train_tld_encoded=self.preprocessors['tld'].transform(self.training_data['tld'])
        x_train_dom_encoded=self.preprocessors['dom'].transform(self.training_data['dom'])
        x_train_numerical_scaled=self.training_data[['digit_cnt','is_https']]
        x_train=hstack([x_train_url_encoded,x_train_tld_encoded,x_train_dom_encoded,x_train_numerical_scaled])

        logger.info("Performed preprocessing on training data")

        self.model.fit(x_train,y_train)
        logger.info("Model training completed")

        if not os.path.exists(self.model_version_filepath):
            save_json(self.model_version_filepath,{'version':1.0})
            self.model_version=1.0
        else:
            model_version=load_json(self.model_version_filepath).version
            self.model_version=float(model_version)+1
            save_json(self.model_version_filepath,{'version':self.model_version})

            
        x_test_url_encoded=self.preprocessors['url'].transform(self.testing_data['url'])
        x_test_tld_encoded=self.preprocessors['tld'].transform(self.testing_data['tld'])
        x_test_dom_encoded=self.preprocessors['dom'].transform(self.testing_data['dom'])
        x_test_numerical_scaled=self.testing_data[['digit_cnt','is_https']]
        x_test=hstack([x_test_url_encoded,x_test_tld_encoded,x_test_dom_encoded,x_test_numerical_scaled])

        y_test=self.testing_data[self.target_feature]
        logger.info(f"Testing started")

        y_pred=self.model.predict(x_test)
        logger.info(f"Testing completed")

        accuracy=accuracy_score(y_test,y_pred)*100
        logger.info(f"Training Score: {self.model.score(x_train,y_train)*100}")
        logger.info(f"Accuracy: {accuracy}")
        report=classification_report(y_test,y_pred,target_names=['Not Phishing','Phising'])
        logger.info(f"Classification report \n {str(report)}")

        mlflow.set_experiment('Phising-Url-Detection')
        with mlflow.start_run(run_name=f'Training Model - v{self.model_version}'):
            mlflow.log_metric('Training Score',self.model.score(x_train,y_train)*100)
            mlflow.log_metric('Accuracy',accuracy)
            mlflow.log_text(str(report),'ClassificationReport.txt')

            mlflow.log_params(self.model.get_params())
            signature=infer_signature(x_train.tocsr(),self.model.predict(x_train))

            if accuracy>90:
                mlflow.sklearn.log_model(
                    sk_model=self.model,
                    name='ClassifierPhisingUrl',
                    signature=signature,
                    input_example=x_train.tocsr(),
                    registered_model_name='PhishingUrlDetector'
                )
                logger.info('The model performance is above the required threshold so it has been added to MLflow model registry')
                save_model(self.inf_model_filepath,self.model)
                logger.info('Model has been saved into artifacts and artifacts-prediction directories')
            else:
                mlflow.sklearn.log_model(
                    sk_model=self.model,
                    name='ClassifierPhisingUrl',
                    signature=signature,
                    input_example=x_train.tocsr()
                )
                logger.info('The model performance is less than the required threshold')

        save_model(self.model_filepath,self.model)
        logger.info(f"Mlflow logging has been completed")
        return self.model 
    


