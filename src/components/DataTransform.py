
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import pandas as pd 
from src.constants import * 
from src.utils.common import * 

class DataTransform:
    def __init__(self):
        self.SCHEMA=load_yaml(SCHEMA_PATH)
        self.TRANSFORMATION_CONFIG=load_yaml(CONFIG_PATH).data_transformation
        
    @ensure_annotations
    def preprocess_data(self,data:pd.DataFrame)->pd.DataFrame:
        scaler=StandardScaler()
        data.drop_duplicates(inplace=True)
        logger.info(f"Removed Duplicates")

        data.dropna(inplace=True)
        logger.info(f"Removed rows containing Null")

        numerical_cols=[]
        categorical_cols=[]
        for col,type in self.SCHEMA.INP_COLS.items():
            if type in ['int64','float64']:
                numerical_cols.append(col)
            else:
                categorical_cols.append(col)

        data[numerical_cols]=scaler.fit_transform(data[numerical_cols])
        
        TRANSFORMED_DATA_PATH=os.path.join(self.TRANSFORMATION_CONFIG.artifacts,self.TRANSFORMATION_CONFIG.complete_transformed_filename)
        create_dirs(Path(self.TRANSFORMATION_CONFIG.artifacts))

        for col in categorical_cols:
            encoder=LabelEncoder()
            data[col]=data[col].astype('str')
            data[col]=encoder.fit_transform(data[col])
            ENCODER_FILEPATH=os.path.join(self.TRANSFORMATION_CONFIG.artifacts,f"{self.TRANSFORMATION_CONFIG.encoder_filename}_{col}.pkl")
            save_model(Path(ENCODER_FILEPATH),encoder)
        
        data.to_csv(TRANSFORMED_DATA_PATH,index=False)
        logger.info(f"Transformed and stored complete data successfully in {TRANSFORMED_DATA_PATH}")

        SCALER_FILEPATH=os.path.join(self.TRANSFORMATION_CONFIG.artifacts,self.TRANSFORMATION_CONFIG.scaler_filename)
        save_model(Path(SCALER_FILEPATH),scaler)
        return data
    
    @ensure_annotations
    def training_testing_data_creation(self,data:pd.DataFrame)->tuple:
        logger.info(f"Total number of rows: {data.shape[0]}")
        train,test=train_test_split(data,test_size=0.2)
        logger.info(f"Train Test split completed")

        logger.info(f"Total number of rows in training data: {train.shape[0]}")
        logger.info(f"Total number of rows in testing data: {test.shape[0]}")

        TRAIN_FILEPATH=os.path.join(self.TRANSFORMATION_CONFIG.artifacts,self.TRANSFORMATION_CONFIG.training_data_filename)
        TEST_FILEPATH=os.path.join(self.TRANSFORMATION_CONFIG.artifacts,self.TRANSFORMATION_CONFIG.testing_data_filename)
        train.to_csv(TRAIN_FILEPATH,index=False)
        logger.info(f"Store the Training data successfully in {TRAIN_FILEPATH}")

        test.to_csv(TEST_FILEPATH,index=False)
        logger.info(f"Store the Testing data successfully in {TEST_FILEPATH}")
        return train,test
