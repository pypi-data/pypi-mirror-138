"""Handling of configuration files"""
import json


def load_json_config(filename: str) -> dict:
    """Load json configuration file.
    :param filename:
        Path to file.
    :return:
        Loaded configuration as a dict.
    """
    if not filename:
        raise ValueError('Filename must be provided.')

    config = None
    with open(filename) as f:
        config = json.load(f)
    return config
