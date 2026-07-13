import os 
import pandas as pd 
import streamlit as st 
import requests 
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT=os.environ['API_URL']

st.set_page_config(layout='wide')

_,col2,col3=st.columns([2,5,2])

with col2:
    st.title(':blue[Phishing Detection using URL]')
st.text('')
st.text('')
url=st.text_input(label=":blue[Please enter the complete URL below]",value=None,placeholder='URL Here')
if url:
    with st.spinner('Analysis in progress...'):
        payload={"url":url}
        response=requests.post(API_ENDPOINT,json=payload)
        result=response.json()
        status_code=response.status_code

        if status_code==200:
            prediction=result.get('prediction')
            dom=result.get('dom')
            tld=result.get('tld')
            is_https=result.get('is_https')
            digit_cnt=result.get('digit_cnt')

            with st.expander(':blue[Information regarding the prediction]'):
                st.markdown(f':green[Identified Domain]: {dom}')
                is_https={0:'No',1:'Yes'}.get(is_https)
                st.markdown(f":green[HTTPS?]: {is_https}")
                st.markdown(f':green[TLD]: {tld}')
                st.markdown(f':green[Number of digits in URL]: {digit_cnt}')

            if prediction=='Not Phishing':
                st.success(f":green[This url's category: {prediction}]")
            else:
                st.success(f":red[This url's category: {prediction}]")
        else:
            st.subheader(f"Inferencing failed - {result.get('response')}")
    


