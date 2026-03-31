import sys

from networksecurity.components.data_ingestion import DataIngestion
from framework.logger import logging
from framework.exception import MyException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
if __name__ == '__main__':
    try:
        print("data ingestion started")
        logging.info("data ingestion started")
        traning_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(traning_pipeline_config)
        data = DataIngestion(data_ingestion_config)
        print("data ingestion initaited")
        print(data.initiate_data_ingestion())



    except Exception as e:
        logging.error(e)
        raise MyException(e,sys)
