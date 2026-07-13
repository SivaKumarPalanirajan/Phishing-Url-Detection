import logging 
import yaml
import json 
from logging import StreamHandler,FileHandler
from datetime import datetime 
import sys 
import os 
from box import ConfigBox 
from box.exceptions import BoxValueError 
from pathlib import Path
import pickle 
from ensure import ensure_annotations
import pandas as pd 

def setup_logger():
    logging_dir='logs'
    log_file_name=f"{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.log"
    complete_log_dir=os.path.join(logging_dir,log_file_name)

    os.makedirs(logging_dir,exist_ok=True)
    LOG_FORMAT="[%(asctime)s] - %(levelname)s - %(module)s - %(message)s"
    logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,
                        handlers=[
                            StreamHandler(sys.stdout),
                            FileHandler(complete_log_dir)
                        ]
                    )
    return logging.getLogger('PhishingUrlDetection')

logger=setup_logger()

def load_yaml(filename:Path)->ConfigBox:
    try:
        with open(filename,'r') as f:
            data=yaml.safe_load(f)
            logger.info(f"Successfully loaded {filename}")
            return ConfigBox(data)
    except BoxValueError:
        logging.exception(f"{filename} is empty")
    except:
        logging.exception(f"{filename} can't be opened")

def load_model(filename:Path)->None:
    try:
        dirname,ext=os.path.splitext(filename)
        if ext in ['.sav','.pkl','.h5']:
            with open(filename,'rb') as f:
                model=pickle.load(f)
                logger.info(f"Successfully loaded {filename}")
            return model
        else:
            logging.error(f"{filename} can't be loaded - invalid filename")
    except:
        logging.exception(f"{filename} can't be loaded")

def load_json(filename:Path)->ConfigBox:
    try:
        with open(filename,'r') as f:
            data=json.load(f)
            logger.info(f"Successfully loaded {filename}")
            return ConfigBox(data)
    except BoxValueError:
        logging.exception(f"{filename} is empty")
    except:
        logging.exception(f"{filename} can't be opened")

def save_json(filename:Path,data:dict)->None:
    try:
        with open(filename,'w') as f:
            json.dump(data,f,indent=2)
            logger.info(f"Successfully saved {filename}")
    except:
        logging.exception(f"{filename} can't be saved")

def save_model(filename:Path,data)->None:
    try:
        dirname,ext=os.path.splitext(filename)
        if ext in ['.sav','.pkl','.h5']:
            with open(filename,'wb') as f:
                pickle.dump(data,f)
                logger.info(f"Successfully saved {filename}")
        else:
            logging.error(f"{filename} can't be saved - invalid filename")
    except:
        logging.exception(f"{filename} can't be saved")

def create_dirs(dirname:Path)->None:
    try:
        os.makedirs(dirname,exist_ok=True)
        logging.info(f"{dirname} was created")
    except:
        logging.exception(f"{dirname} can't be created")