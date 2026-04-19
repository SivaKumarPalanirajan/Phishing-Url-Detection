import os 
from pathlib import Path 
import logging 

LOG_FORMAT="[%(asctime)s] - %(levelname)s - %(module)s - %(message)s"
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT)

paths=[Path(dir) for dir in [
    f"src/__init__.py",
    f"src/components/__init__.py",
    f"src/pipelines/__init__.py",
    f"src/notebooks/ingestion.ipynb",
    f"src/constants/__init__.py",
    f"src/utils/__init__.py",
    f"src/utils/common.py",
    'params.yaml',
    'config.yaml',
    'schema.yaml',
    'main.py',
    'Dockerfile',
    'app.py'
]
]

for dir in paths:
    dirname,filename=os.path.split(dir)
    if dirname!="":
        os.makedirs(dirname,exist_ok=True)

    if not os.path.exists(dir) or os.path.getsize(dir)==0:
        with open(dir,'w') as f:
            pass 
        if dirname!='':
            logging.info(f"Created file {filename} in {dirname}")
        else:
            logging.info(f"Created file {filename}")



