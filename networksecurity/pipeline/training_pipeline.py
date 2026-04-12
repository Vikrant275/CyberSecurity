import sys,json,os

from framework.logger import logging
from framework.exception import MyException


from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, \
    ModelTraningConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig #TestingPipelineConfig

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.artifact_entitiy import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainingArtifact,ClassificationMetricsArtifact

import warnings

from networksecurity.pipeline.batch_prediction import PredictionPipeline
from networksecurity.utils.utils import save_json

warnings.filterwarnings('ignore')


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        # self.test_pipeline_config = TestingPipelineConfig()


    def start_data_ingestion(self):
        try:
            logging.info("Starting data ingestion")
            print("Starting data ingestion")

            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion initiated and artifact: {data_ingestion_artifact}")
            print(f"Data ingestion initiated and artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)


    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info("Starting data validation")
            print("Starting data validation")
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data validation initiated and artifact: {data_validation_artifact}")
            print(f"Data validation initiated and artifact: {data_validation_artifact}")

            return data_validation_artifact
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            logging.info("Starting data transformation")
            print("Starting data transformation")
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data transformation initiated and artifact: {data_transformation_artifact}")
            print(f"Data transformation initiated and artifact: {data_transformation_artifact}")

            return data_transformation_artifact
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

    def start_model_training(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info("Starting model training")
            print("Starting model training")
            self.model_training_config = ModelTraningConfig(training_pipeline_config=self.training_pipeline_config)
            train_model = ModelTrainer(data_transformation_artifact=data_transformation_artifact,model_trainer_config=self.model_training_config)
            train_model_artifact = train_model.initiate_model_training()
            logging.info(f"Model training initiated and artifact: {train_model_artifact}")
            print(f"Model training initiated and artifact: {train_model_artifact}")

            return train_model_artifact
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

    def start_pipeline(self):
        try:
            logging.info("Starting pipeline training")
            print("Starting pipeline training")
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_training_artifact = self.start_model_training(data_transformation_artifact)
            logging.info(f"training pipeline completed successfully")
            print(f"training pipeline completed successfully with model training artifact: {model_training_artifact}")

            artifacts_dic = {
                'model_name': model_training_artifact.model_name,
                'trained_model_file_path': model_training_artifact.trained_model_file_path,
                'train_metrics_artifact': model_training_artifact.train_metrics_artifact.__dict__,
                'test_metrics_artifact': model_training_artifact.test_metrics_artifact.__dict__

            }

            model_info_file_path = os.path.join(self.training_pipeline_config.model_information,'model_info.json')
            save_json(file_path=model_info_file_path,obj=artifacts_dic)

            return artifacts_dic

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

if __name__ == '__main__':
    pipeline = TrainingPipeline()
    pipeline.start_pipeline()

