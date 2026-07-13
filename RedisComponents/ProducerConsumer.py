import redis 
import json 
import hashlib 
from src.utils.common import logger,create_dirs
from argparse import ArgumentParser
import os 

if __name__=="__main__":
    r=redis.Redis(host='localhost',port=6379,decode_responses=True)

    parser=ArgumentParser()
    parser.add_argument('--mode',required=True,choices=['producer','consumer'])
    parser.add_argument('--inp-url',type=str)
    parser.add_argument('--out-dir',type=str)

    args=parser.parse_args()
    
    if args.mode=='producer':

        url=str(args.inp_url)

        id=hashlib.sha256(url.encode()).hexdigest()
        r.hset(id,mapping={
            "url": url,
            "retries": 0
        })
        r.lpush('MainQueue-PhishingUrl',id)
        logger.info(f"PRODUCER ---- Moved job to Main Queue {id} ---- Content: {url}")

    elif args.mode=='consumer':
        while True:
            result = r.brpop('ResultQueue-PhishingUrl',timeout=5)

            if result:
                _ , taskid=result 

                complete_data=r.hgetall(str(taskid))

                create_dirs(args.out_dir)

                with open(os.path.join(args.out_dir,f"{taskid}.json"),'w') as f:
                    json.dump(complete_data,f)

                logger.info(f'Consumer ---- Saved Json ---- ID: {taskid}')            
            else:
                logger.info('Consumer ---- Empty Result Queue')            
