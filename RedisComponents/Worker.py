import redis 
import json 
from src.utils.common import logger
import pickle 
from scipy.sparse import hstack
import tldextract
import os 

MAX_RETRIES=3 

model=pickle.load(open(os.path.join('artifacts-prediction','model.pkl'),'rb'))
logger.info(f'Worker ---- Loaded model')

if __name__=='__main__':
    r=redis.Redis(host='localhost',port=6379,decode_responses=True)
    while True:
        taskid=r.brpoplpush('MainQueue-PhishingUrl','ProcessingQueue-PhishingUrl',timeout=5)

        if taskid:
            data=r.hgetall(taskid)
            url=data['url']
            logger.info(f'Worker ---- Picked up Job ---- ID: {taskid} ---- Url: {url}')   

            try:

                if url is not None:
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
                logger.info('Worker ---- Created new features')

                for col in ['dom','tld','url']:
                    encoder_path=os.path.join('artifacts-prediction',f'dataencoder_{col}.pkl') 
                    encoder=pickle.load(open(encoder_path,'rb'))
                    logger.info(f'Worker ---- Loaded {col} encoder')
                    if col=='dom':
                        dom_encoded=encoder.transform([dom])[0]
                    elif col=='tld':
                        tld_encoded=encoder.transform([tld])[0]
                    elif col=='url':
                        url_encoded=encoder.transform([url])[0]

                logger.info(f'Worker ---- Encoded features')

                scaler_path=os.path.join('artifacts-prediction','datascaler.pkl') 
                scaler=pickle.load(open(scaler_path,'rb'))
                logger.info(f'Worker ---- Loaded scaler')

                numerical_vals=scaler.transform([[digit_cnt,is_https]])[0]
                logger.info(f'Worker ---- Performed scaling')

                inp_vals=hstack([url_encoded,tld_encoded,dom_encoded,numerical_vals])
                prediction=model.predict(inp_vals)[0]

                logger.info(f'Worker ---- Inferencing completed')
                
                prediction_value={0:'Not Phishing',1:'Phishing'}.get(prediction)
                data['result']=prediction_value

                r.lpush('ResultQueue-PhishingUrl',str(taskid))
                r.hset(str(taskid),mapping=data)
                r.lrem('ProcessingQueue-PhishingUrl',-1,str(taskid))
                logger.info(f'Worker ---- Moved Job to Result Queue ---- ID: {taskid} ---- Url: {url}')   

            except Exception as e:
                r.lrem('ProcessingQueue-PhishingUrl',-1,str(taskid))

                if int(data['retries']) < MAX_RETRIES:
                    data['retries']=int(data['retries'])+1
                    r.lpush('MainQueue-PhishingUrl',str(taskid))
                    r.hset(str(taskid),mapping=data)
                    logger.exception(f'Worker ---- Moved Job to Main Queue ---- ID: {taskid} Error: {e}')            

                else:
                    r.lpush('DLQ-PhishingUrl',str(taskid))
                    logger.exception(f'Worker ---- Moved Job to DLQ ---- ID: {taskid} Error: {e}')            

        else:
            logger.info('Worker ---- Empty MainQueue')            

