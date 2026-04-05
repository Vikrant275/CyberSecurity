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

SCHEMA_FILE_NAME :str = os.path.join(GetConfig(config_file='config_path.yaml',variables='schema_data').get(),
                                     GetConfig(config_file='config_file.yaml',variables='schema_file').get()
                                     )

'''
Data validation related constant variables
'''
DATA_VALIDATION_DIR_NAME :str = 'validation_data'
DATA_VALIDATION_VALID_DIR :str = 'validated'
DATA_VALIDATION_INVALID_DIR :str = 'invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR :str = 'report_drift'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME : str = 'report.yaml'

'''
Data Transformation related variables
'''
DATA_TRANSFORMATION_DIR_NAME :str = 'transformation_dir'
DATA_TRANSFORMATION_TRAIN_FILE :str = GetConfig(config_file='config_file.yaml',variables='transformed_train').get()
DATA_TRANSFORMATION_TEST_FILE :str = GetConfig(config_file='config_file.yaml',variables='transformed_test').get()
DATA_TRANSFORMATION_OBJECT_FILE :str = GetConfig(config_file='config_file.yaml',variables='transformed_obj').get()
##  knn imputer to replace nan value
DATA_TRANSFORMATION_IMPUTER_PARAMS : dict = {
    'missing_values' : np.nan,
    'n_neighbors' : 3,
    'weights' : 'uniform'
}