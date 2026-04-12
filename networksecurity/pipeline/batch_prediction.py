from framework.exception import MyException
from framework.logger import logging
import pandas as pd
import os,sys

from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.utils.utils import *


class PredictionPipeline:
    def __init__(self,test_data:pd.DataFrame):
        self.test_data = test_data
        self.training_pipeline_config = TrainingPipelineConfig()

    def get_model(self,model_info_file_path:str):
        try:
            model_info = load_json(model_info_file_path)
            return model_info['trained_model_file_path']
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)


    def predict(self):
        try:
            model_information_path = os.path.join(self.training_pipeline_config.model_information, 'model_info.json')
            model_path = self.get_model(model_info_file_path=model_information_path)
            model = load_object(model_path)

            return model.predict(x=self.test_data)


        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)



if __name__ == '__main__':
    test_data = pd.read_csv('D:\\PythonProject3\\CyberSecurity\\artifacts\\04_12_2026_19_45_07\\validation_data\\validated\\test.csv')
    x_test = test_data.drop(columns=['Result'])

    print(PredictionPipeline(x_test).predict())