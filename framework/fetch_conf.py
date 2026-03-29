import yaml
import os

def load_config(config_file):
    config_file_path = os.path.join('D:\\PythonProject3\\CyberSecurity\\networksecurity\\config',config_file)

    with open(config_file_path, 'r') as f:
        config = yaml.load(f,Loader=yaml.FullLoader)

    if config is None:
        raise FileNotFoundError(f"{config_file} Config file not found at D:\\PythonProject3\\CyberSecurity\\networksecurity\\config")
    else:
        return config


def get_config(config_file,var):
    if var not in config_file:
        try:
            config = load_config(config_file)
        except FileNotFoundError:
            raise FileNotFoundError(config_file)

        content = config.get(var,{})
        if content is None:
            raise Exception(f"{var} Config file not found at {config_file}")
        else:
            return content





class GetConfig:
    def __init__(self,config_file=None,variables=None):
        self.config_file=config_file
        self.variables=variables
        self.content=get_config(config_file,variables)

    def get(self):
        return self.content

