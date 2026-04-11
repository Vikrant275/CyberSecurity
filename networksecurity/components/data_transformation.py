import os,sys
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.train_pipeline import TARGET_COL,DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entitiy import DataValidationArtifact,DataTransformationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig

from framework.logger import logging
from framework.exception import MyException

from networksecurity.utils.utils import *

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

    @staticmethod
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            logging.info('Reading data from file')
            return pd.read_csv(file_path)
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

    def get_data_transformation_pipeline(self) -> Pipeline:
        '''
        This function
        :return:
        '''
        try:
            logging.info('Getting data transformation pipeline')
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info('Imputer initialized successfully')

            preprocessor :Pipeline = Pipeline([('imputer', imputer)])

            return preprocessor
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)


    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info('Initiating data transformation')
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            #traing features
            input_training_features = train_df.drop(columns=[TARGET_COL])
            target_training_features = train_df[TARGET_COL]
            target_training_features = target_training_features.replace(-1,0)

            # testing features
            input_testing_features = test_df.drop(columns=[TARGET_COL])
            target_testing_features = test_df[TARGET_COL]
            target_testing_features = target_testing_features.replace(-1,0)

            preprocessor = self.get_data_transformation_pipeline()
            transformed_train = preprocessor.fit_transform(input_training_features)
            transformed_test = preprocessor.transform(input_testing_features)

            train_arr = np.c_[transformed_train,target_training_features]
            test_arr = np.c_[transformed_test,target_testing_features]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)

            save_object(file_path='final_preprocessor/preprocessor.pkl',obj=preprocessor)

            #prepraing artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path,
            )

            return data_transformation_artifact
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)
