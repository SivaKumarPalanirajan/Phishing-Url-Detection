from src.pipelines.PredictionPipeline import PredictionPipeline
from src.utils.common import * 
import os 
import pandas as pd 
import streamlit as st 

st.title('Phishing Detection using URL')

url=st.text_input(label='URL',value=None,placeholder='Please enter the complete url here')
if url:
    a=PredictionPipeline()
    prediction=a.start_prediction(url)
    if prediction=='Not Phishing':
        st.subheader(f":green[This url's category: {prediction}]")
    else:
        st.subheader(f":red[This url's category: {prediction}]")


