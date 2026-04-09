import sys

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from framework.logger import logging
from framework.exception import MyException
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig,DataTransformationConfig,ModelTraningConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_transformation import DataTransformation
import warnings


from networksecurity.entity.artifact_entitiy import DataTransformationArtifact
if __name__ == '__main__':
    try:
        warnings.filterwarnings("ignore")
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

        print("model training started")
        # data_transformation_artifact = DataTransformationArtifact(transformed_object_file_path='D:\\PythonProject3\\CyberSecurity\\artifacts\\04_09_2026_19_53_43\\transformation_dir\\preprocessing.pkl', transformed_train_file_path='D:\\PythonProject3\\CyberSecurity\\artifacts\\04_09_2026_19_53_43\\transformation_dir\\train.npy', transformed_test_file_path='D:\\PythonProject3\\CyberSecurity\\artifacts\\04_09_2026_19_53_43\\transformation_dir\\test.npy')
        model_training_config = ModelTraningConfig(traning_pipeline_config)
        model_trainer_artifact = ModelTrainer(data_transformation_artifact,model_training_config).initiate_model_training()
        print("model training initaited successfully")
        print(model_trainer_artifact)




    except Exception as e:
        logging.error(e)
        raise MyException(e,sys)
