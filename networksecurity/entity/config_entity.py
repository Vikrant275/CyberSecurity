from datetime import datetime
import os
from framework.logger import logging
from framework.exception import MyException
from networksecurity.constant.train_pipeline import *


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        try:
            timestamp = timestamp.strftime('%m_%d_%Y_%H_%M_%S')
            self.pipeline_name = PIPELINE_NAME
            self.artifact_name = ARTIFACT_DIR
            self.artifact_dir = os.path.join(self.artifact_name,timestamp)
            self.timestamp : str= timestamp
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

class DataIngestionConfig:
    def __init__(self,training_pipeline_config):
        self.training_pipeline_config = TrainingPipelineConfig()

        self.data_ingestion_dir :str = os.path.join(
            training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME
        )
        self.feature_file_path :str= os.path.join(
            self.data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR
        )
        self.train_file_path :str= os.path.join(
            self.data_ingestion_dir,TRAIN_FILE_NAME
        )
        self.test_file_path :str= os.path.join(
            self.data_ingestion_dir,TEST_FILE_NAME
        )
        self.train_test_split_ratio : float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name = DATA_INGESTION_COLLECTION_NAME
        self.database_name = DATA_INGESTION_DATABASE_NAME