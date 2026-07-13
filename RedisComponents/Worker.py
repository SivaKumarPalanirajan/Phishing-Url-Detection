import redis 
import json 
from src.utils.common import logger
from src.pipelines.PredictionPipeline import PredictionPipeline 

MAX_RETRIES=3 

if __name__=='__main__':
    r=redis.Redis(host='localhost',port=6379,decode_responses=True)
    while True:
        taskid=r.brpoplpush('MainQueue-PhishingUrl','ProcessingQueue-PhishingUrl',timeout=5)

        if taskid:
            data=r.hgetall(taskid)
            url=data['url']
            logger.info(f'Worker ---- Picked up Job ---- ID: {taskid} ---- Url: {url}')   

            try:
                a=PredictionPipeline()
                prediction,dom,tld,dom,is_https,digit_cnt=a.start_prediction(url)
                data['result']=prediction
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

