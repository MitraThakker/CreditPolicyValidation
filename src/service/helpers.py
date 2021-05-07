from typing import Dict

import yaml


def read_yaml(file_path: str) -> Dict:
    with open(file_path) as yaml_file:
        return yaml.safe_load(yaml_file)


def validate_config(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError):
            raise yaml.YAMLError
    return inner


def main():
    pass


if __name__ == '__main__':
    main()
