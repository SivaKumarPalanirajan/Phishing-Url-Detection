import os 
import pandas as pd 
import streamlit as st 
import requests 
from dotenv import load_dotenv
import time 
import logging 

logging.basicConfig(format='[%(asctime)s] - %(levelname)s - %(module)s - %(lineno)d  - %(message)s',
                    level=logging.INFO)

load_dotenv()

API_ENDPOINT=os.environ['API_URL']

MAX_WAITING_TIME=90 

st.set_page_config(layout='wide')

_,col2,col3=st.columns([2,5,2])

logging.info('Started app')

error_msg=None
with col2:
    st.title(':blue[Phishing Detection using URL]')
st.text('')
st.text('')
url=st.text_input(label=":blue[Please enter the complete URL below]",value=None,placeholder='URL Here')
if url:
    with st.spinner('Analysis in progress...'):
        payload={"url":url}
        START=time.time()
        while time.time() - START < MAX_WAITING_TIME:
            try:
                logging.info('Sending request for inferencing')

                response=requests.post(API_ENDPOINT,json=payload,timeout=15)
                status_code=response.status_code

                if status_code==200 and response.content:
                    result=response.json()
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
                    logging.info('Inferencing successful')
                    break
                    
                else:
                    if response.content:
                        try:
                            logging.error(f"Inferencing failed with status code {response.status_code} - {response.json().get('response')}")
                            error_msg=f"Inferencing failed - {response.json().get('response')}"
                        except Exception as e:
                            logging.error(f"Inferencing failed with status code {response.status_code} - {response.content}")
                            error_msg=f"Inferencing failed - {response.content}"

            except requests.exceptions.Timeout as e:
                logging.exception(f"Inferencing failed - Timeout - {e}")
                error_msg='Inferencing failed - Server timeout'
            
            except requests.exceptions.ConnectionError as e:
                logging.exception(f"Inferencing failed - Connection error - {e}")
                error_msg='Inferencing failed - Connection error'
            
            except Exception as e:
                logging.exception(f"Inferencing failed - {e}")
                error_msg='Inferencing failed - please try again later'
            
        if error_msg is not None:
            st.subheader(error_msg)