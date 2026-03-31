from framework.exception import MyException
from framework.logger import logging

# configuration of the data ingestion config
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entitiy import DataIngestionArtifact

import os
import sys
from typing import List
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

import pymongo
from dotenv import load_dotenv
load_dotenv() # mongodb url fetch from .env

MONGODB_URL = os.getenv('MONGO_DB_URL')

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)


    def export_collection_as_dataframe(self):
        '''
        This function work as fetch data from MongoDB and export it as dataframe.
        :param self:
        :return: dataframe
        '''

        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGODB_URL)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():    # in mongodb database _id columns present that's why we don't required its
                df=df.drop(columns=['_id'])

            df.replace({'na':np.nan},inplace=True)  #whenever get from mongodb in database there are na value after import as dataframe convert in nan value
            return df
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)


    def export_dataframe_into_feature_store(self,dataframe: pd.DataFrame):
        '''
        This function work as fetch data as dataframe and export it as feature store at local path.
        :param dataframe:
        :return: feature_store_file_path dataframe
        '''
        try:
            feature_store_file_path = self.data_ingestion_config.feature_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)  #creating dir
            dir_path = None
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)


    def split_dataframe_into_train_test(self,dataframe: pd.DataFrame):
        '''
        This function work as fetch data as dataframe and split into train and test set.
        :param dataframe:
        '''
        try:
            train_set,test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info(f"Train set size: {len(train_set)} and test set size: {len(test_set)}")

            train_set.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            logging.info(f"export train data to [{self.data_ingestion_config.train_file_path}] path")

            test_set.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            logging.info(f"export test data to [{self.data_ingestion_config.test_file_path}] path")

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)


    def initiate_data_ingestion(self):
        '''
        This function initiate data ingestion process.
        :return:
        '''
        try:
            dataframe = self.export_dataframe_into_feature_store(self.export_collection_as_dataframe())
            self.split_dataframe_into_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.train_file_path,test_file_path=self.data_ingestion_config.test_file_path)

            return data_ingestion_artifact

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)


