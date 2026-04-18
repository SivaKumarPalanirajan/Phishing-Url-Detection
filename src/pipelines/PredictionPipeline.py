import pandas as pd 
import os 
from src.utils.common import load_model,load_yaml 
from typing import List 
import re 
from pathlib import Path 

class PredictionPipeline:
    def __init__(self):    
        self.model=load_model(Path('artifacts-prediction/model.pkl'))
    
    def start_prediction(self,url)->str:
        if url.startswith("https"):
            is_https=1
        else:
            is_https=0
        digit_cnt=0
        for i in url:
            if i.isnumeric():
                digit_cnt+=1
        match = re.search(r'www\.([^/]+)', url)
        if match:
            dom=match.group(1)
            tdl_split=dom.split(".")
            if len(tdl_split)==2:
                tld=tdl_split[-1]
            else:
                tld=".".join(tdl_split[-2:])
        else:
            dom='None'
            tld='None'
        for col in ['dom','tld','url']:
            encoder=load_model(Path(os.path.join('artifacts-prediction',f"dataencoder_{col}.pkl")))
            if col=='dom':
                dom=encoder.transform([dom])[0]
            elif col=='tld':
                tld=encoder.transform([tld])[0]
            elif col=='url':
                url=encoder.transform([url])[0]
        scaler=load_model(Path(os.path.join('artifacts-prediction','datascaler.pkl')))
        numerical_vals=scaler.transform([[digit_cnt,is_https]])[0]
        digit_cnt=numerical_vals[0]
        is_https=numerical_vals[1]
        prediction=self.model.predict([[url,dom,is_https,tld,digit_cnt]])[0]
        return {0:'Not Phishing',1:'Phishing'}.get(prediction)