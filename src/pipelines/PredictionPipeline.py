import pandas as pd 
import os 
from src.utils.common import load_model,load_yaml 
from typing import List 
import re 
from pathlib import Path 
from scipy.sparse import hstack
import tldextract

class PredictionPipeline:
    def __init__(self):    
        self.model=load_model(Path('artifacts-prediction/model.pkl'))
    
    def start_prediction(self,url)->tuple:
        if url.startswith("https"):
            is_https=1
        else:
            is_https=0
        digit_cnt=0
        for i in url:
            if i.isnumeric():
                digit_cnt+=1

        ext = tldextract.extract(url)
        dom,tld=ext.domain+"."+ext.suffix, ext.suffix
        for col in ['dom','tld','url']:
            encoder=load_model(Path(os.path.join('artifacts-prediction',f"dataencoder_{col}.pkl")))
            if col=='dom':
                dom_encoded=encoder.transform([dom])[0]
            elif col=='tld':
                tld_encoded=encoder.transform([tld])[0]
            elif col=='url':
                url_encoded=encoder.transform([url])[0]
        scaler=load_model(Path(os.path.join('artifacts-prediction','datascaler.pkl')))
        numerical_vals=scaler.transform([[digit_cnt,is_https]])[0]
        inp_vals=hstack([url_encoded,tld_encoded,dom_encoded,numerical_vals])
        prediction=self.model.predict(inp_vals)[0]
        return {0:'Not Phishing',1:'Phishing'}.get(prediction),dom,tld,dom,is_https,digit_cnt