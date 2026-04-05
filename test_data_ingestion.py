import sys

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from framework.logger import logging
from framework.exception import MyException

from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.components.data_transformation import DataTransformation

if __name__ == '__main__':
    try:
        print("data ingestion started")
        traning_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(traning_pipeline_config)
        data = DataIngestion(data_ingestion_config)

        data_artifact = data.initiate_data_ingestion()
        print("data ingestion initaited successfully")
        print(data_artifact)

        print("data validation started")
        data_validation_config = DataValidationConfig(traning_pipeline_config)
        data_validation = DataValidation(data_artifact,data_validation_config).initiate_data_validation()
        print("data validation initaited successfully")
        print(data_validation)

        print('data training started')
        data_transformation = DataTransformation(data_validation,DataTransformationConfig(traning_pipeline_config))
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print("data transformation initaited successfully")
        print(data_transformation_artifact)






    except Exception as e:
        logging.error(e)
        raise MyException(e,sys)
