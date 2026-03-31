import pandas as pd
import numpy as np
import pymongo
import json
from framework.logger import logging
from framework.exception import MyException
import os
import sys

import certifi  #it package provide set root certificate, it needs to  make secure HTTPS connection
from dotenv import load_dotenv


load_dotenv()
mongo_url = os.getenv("MONGO_DB_URL")
print(mongo_url)

#ca ---> certificate authority
ca = certifi.where()  #it retrieves part to bundles of ca certificate provide by certifi


class CyberSecurityDataExtractor:
    def __init__(self):
        try:
            pass
        except Exception as e:
            logging.error(e)
            raise MyException(sys,e)

    def csv_to_json(self,file_path):
        try:
            data = pd.read_csv(file_path).reset_index(drop=True)
            records = list(json.loads(data.T.to_json()).values())       #records = df.to_dict(orient="records") This gives the same result without transposing or going through JSON.
            return records
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

    def insert_data_to_mongodb(self,records,database_name,collection_name):
        try:
            self.mongo_client = pymongo.MongoClient(mongo_url)
            self.database_name = database_name
            self.collection_name = collection_name
            self.records = records

            self.database = self.mongo_client[self.database_name]
            self.collection = self.database[collection_name]
            self.collection.insert_many(self.records)
            return(len(records))

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

if __name__ == '__main__':
    file_path = 'D:\\PythonProject3\\CyberSecurity\\network_Data\\phisingData.csv'
    DATABASE = 'vikrant'
    collection_name = 'phisingData'
    cyber_security = CyberSecurityDataExtractor()
    records = cyber_security.csv_to_json(file_path)
    no_of_records = cyber_security.insert_data_to_mongodb(records,DATABASE,collection_name)
    print(no_of_records)
