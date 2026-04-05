import os,sys,yaml

from networksecurity.utils.utils import *

from framework.logger import logging
from framework.exception import MyException
from framework.fetch_conf import GetConfig
from networksecurity.constant.train_pipeline import *

import pandas as pd

class MakeSchema:
    def __init__(self):
        try:
            self.schema_file_name :str = SCHEMA_FILE_NAME
            self.orignal_data=  os.path.join(
                GetConfig(config_file='config_path.yaml',variables='input_data').get(),
                GetConfig(config_file='config_file.yaml',variables='input_data').get(),
            )
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

    def initialize_cols(self):
        try:
            df = pd.read_csv(self.orignal_data)
            columns = df.columns
            dt = list(df.dtypes)
            load_data = {
                'columns': {columns[i]: str(dt[i]) for i in range(len(columns))},
            }

            try:
                logging.info('Initializing schema')
                # create_schema(self.schema_file_name)
                #
                # dump_schema(self.schema_file_name,load_data)
                write_yaml(self.schema_file_name, load_data, replace=True)
            except Exception as e:
                logging.error(e)
                raise MyException(e,sys)

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

    def initialize_numerical(self):
        try:
            df = pd.read_csv(self.orignal_data)
            num_cols = df.select_dtypes(include=[np.number]).columns

            load_data = {
                'numerical_columns':[col for col in num_cols]
            }

            try:
                write_yaml(self.schema_file_name,load_data)
            except Exception as e:
                logging.error(e)
                raise MyException(e,sys)

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)


if __name__ == '__main__':
    make = MakeSchema()
    make.initialize_cols()
    make.initialize_numerical()