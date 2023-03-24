import yaml
import json
import os
import sys


def yaml_to_json(file_name):
    with open(file_name, 'r') as file:
        configuration = yaml.safe_load(file)
        return configuration


def load_json(file_name):
    current_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.dirname(os.path.abspath("API.py")) + file_name) as user_file:
        greetings = user_file.read()
    parsed_json = json.loads(greetings)
    return parsed_json


if __name__ == "__main__":
    print(yaml_to_json("config.yaml"))


