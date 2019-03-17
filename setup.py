import configparser
import os

config_dir = 'config'
os.makedirs(config_dir, exist_ok=True)

config = configparser.ConfigParser()
config['DEFAULT'] = {}

config['DEFAULT']['api_key'] = input("API Key: ")
config['DEFAULT']['light_id'] = input("Light Bulb id: ")

with open(f"{config_dir}/lifx.ini", 'w') as configfile:
    config.write(configfile)
