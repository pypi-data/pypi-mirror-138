import yaml
import logging
import os

def read_yaml(yaml_file_path: str) -> dict:
    with open(yaml_file_path) as yaml_file:
        file_data=yaml.safe_load(yaml_file)
    return file_data
