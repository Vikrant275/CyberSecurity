from networksecurity.entity.artifact_entitiy import DataIngestionArtifact ,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig

from framework.logger import logging
from framework.exception import MyException

from networksecurity.constant.train_pipeline import *
from networksecurity.utils.utils import *

from scipy.stats import ks_2samp  #check weather data drift or not
import pandas as ps
import os,sys


class DataValidation:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml(SCHEMA_FILE_NAME)
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)


    def initiate_data_validation(self)->DataValidationArtifact:
        try:

            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            #read data from train and test
            logging.info("Reading training data from file")
            train_df = DataValidation.read_data(train_file_path)

            logging.info("Reading test data from file")
            test_df = DataValidation.read_data(test_file_path)

            status_report = {}
            # Validate no. of columns
            status = validate_num_cols(self._schema_config['columns'],train_df)
            if not status:
                error_message = f"Number of columns does not match number of columns in dataframe"
                status_report.update({'validate_num_col': {'train_df': {
                    error_message: status}}})

            status = validate_num_cols(self._schema_config['columns'],test_df)
            if not status:
                error_message = f"Number of columns does not match number of columns in dataframe"
                status_report.update({'validate_num_col': {'test_df':{
                    error_message: status}}})

            # validate null
            status = validate_is_null(train_df)
            if not status:
                error_message = f"Number of null values does not match number of columns in dataframe"
                status_report.update({'validate_null_col': {'train_df': {
                    error_message: status}}})

            status = validate_is_null(test_df)
            if not status:
                error_message = f"Number of null values does not match number of columns in dataframe"
                status_report.update({'validate_null_col': {'test_df': {
                    error_message: status}}})

            # Validate numeric columns
            status = validate_is_numeric(self._schema_config['numerical_columns'],train_df)
            if not status:
                error_message = f"Number of numeric values does not match number of columns in dataframe"
                status_report.update({'validate_numeric_col': {'train_df': {
                    error_message: status}}})

            status = validate_is_numeric(self._schema_config['numerical_columns'],test_df)
            if not status:
                error_message = f"Number of numeric values does not match number of columns in dataframe"
                status_report.update({'validate_numeric_col': {'test_df': {
                    error_message: status}}})

            #check data drift
            status = detect_dataset_drift(train_df,test_df,self.data_validation_config.drift_report_file_path)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                validate_report=status_report,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)