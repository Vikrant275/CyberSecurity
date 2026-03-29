import logging
import os
import sys
from datetime import datetime
from framework.fetch_conf import GetConfig

script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
LOG_FILE=f"{script_name}_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


log_path = GetConfig('config_path.yaml',variables='log').get()
os.makedirs(log_path,exist_ok=True)
LOG_FILE_PATH= os.path.join(log_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level = logging.DEBUG,
    format = f'%(asctime)s - %(levelname)s - %(message)s - {script_name} - %(lineno)d'
)

