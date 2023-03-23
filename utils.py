import yaml
import json


def yaml_to_json(file_name):
    with open(file_name, 'r') as file:
        configuration = yaml.safe_load(file)
        return configuration


if __name__ == "__main__":
    print(yaml_to_json("config.yaml"))

