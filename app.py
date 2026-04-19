from src.pipelines.PredictionPipeline import PredictionPipeline
from src.utils.common import * 
import os 
import pandas as pd 
import streamlit as st 
st.set_page_config(layout='wide')

_,col2,col3=st.columns([2,5,2])

with col2:
    st.title(':blue[Phishing Detection using URL]')
st.text('')
st.text('')
url=st.text_input(label=":blue[Please enter the complete URL below]",value=None,placeholder='URL Here')
if url:
    a=PredictionPipeline()
    prediction,dom,tld,dom,is_https,digit_cnt=a.start_prediction(url)
    with st.spinner('Analysis in progress...'):
        with st.expander(':blue[Information regarding the prediction]'):
            values={'Domain':dom,'TLD':tld,'HTTPS?':{0:'No',1:'Yes'}.get(is_https),'Number of digits':digit_cnt}
            st.table(pd.DataFrame(data=values,index=[0]),hide_index=True)
        if prediction=='Not Phishing':
            st.success(f":green[This url's category: {prediction}]")
        else:
            st.success(f":red[This url's category: {prediction}]")
    


