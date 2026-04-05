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

class DataValidationConfig:
    def __init__(self,training_pipeline_config):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_dir = os.path.join(
            self.data_validation_dir,DATA_VALIDATION_VALID_DIR
        )
        self.invalid_data_dir = os.path.join(
            self.data_validation_dir,DATA_VALIDATION_INVALID_DIR
        )
        self.valid_train_file_path : str= os.path.join(
            self.valid_data_dir,TRAIN_FILE_NAME
        )
        self.valid_test_file_path : str= os.path.join(
            self.valid_data_dir,TEST_FILE_NAME
        )
        self.invalid_train_file_path : str= os.path.join(
            self.invalid_data_dir,TRAIN_FILE_NAME
        )
        self.invalid_test_file_path : str= os.path.join(
            self.invalid_data_dir,TEST_FILE_NAME
        )
        self.drift_report_file_path : str = os.path.join(
            self.valid_data_dir,
            DATA_VALIDATION_DRIFT_REPORT_DIR,
            DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )

class DataTransformationConfig:
    def __init__(self,training_pipeline_config):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path : str= os.path.join(self.data_transformation_dir,DATA_TRANSFORMATION_TRAIN_FILE)
        self.transformed_test_file_path : str = os.path.join(self.data_transformation_dir,DATA_TRANSFORMATION_TEST_FILE)
        self.transformed_object_file_path :str = os.path.join(self.data_transformation_dir,DATA_TRANSFORMATION_OBJECT_FILE)