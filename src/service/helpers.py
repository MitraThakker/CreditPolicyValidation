from typing import Dict

import yaml


def read_yaml(file_path: str) -> Dict:
    """
    Parses YAML file from the given path and returns a corresponding dictionary object.
    """
    with open(file_path) as yaml_file:
        return yaml.safe_load(yaml_file)


def validate_config(func):
    """
    Can be used as a decorator around any function or method that uses the config.
    It'll raise a `yaml.YAMLError` if the decorated function or method does the following:
    1. Access a field that doesn't exist.
    2. Type cast a field's value with an incompatible data type.

    Usage:

        @validate_config
        def function_name(...):
            ...
            # Code that uses the config values
            ...

    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, TypeError):
            raise yaml.YAMLError

    return inner
