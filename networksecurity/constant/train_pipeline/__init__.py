import os
import sys
import numpy as np
import pandas as pd
from framework.fetch_conf import GetConfig

'''
Data Ingestion related constant variables 
'''
DATA_INGESTION_COLLECTION_NAME : str= 'phisingData'
DATA_INGESTION_DATABASE_NAME : str= 'vikrant'
DATA_INGESTION_DIR_NAME : str= 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR : str= 'feature_store'
DATAINGESTION_INGESTED_DIR : str= 'ingested_data'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO : float= 0.25

'''
defining common constant variables for training pipeline 
'''

TARGET_COL : str= 'Result'
PIPELINE_NAME :str = 'cybersecurity_pipeline'
ARTIFACT_DIR : str = GetConfig(config_file='config_path.yaml',variables='artifact').get()
FILE_NAME : str = GetConfig(config_file='config_file.yaml',variables='input_data').get()

TRAIN_FILE_NAME : str = GetConfig(config_file='config_file.yaml',variables='train_file').get()
TEST_FILE_NAME : str = GetConfig(config_file='config_file.yaml',variables='test_file').get()
