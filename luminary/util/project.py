import configparser
import os


def load_config(config_name):
    config = configparser.ConfigParser()
    config_dir = f"{os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}/config"
    config.read(f"{config_dir}/{config_name}")
    return config
