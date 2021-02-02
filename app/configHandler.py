import json
from typing import List
from pathlib import Path


class Config:
    """
    This class is a template for Configurations whose atributes will be added directly the instance of this class. Property [properties] contain all attributes that config should have.
    """
    properties: List[str] = [
        'log_to_file',
        'log_to_console',
        'console_logger_type',
        'log_library',
        'console_log_level',
        'file_log_level',
        'library_log_level',
        'discord_token_file'
    ]


def loadConfig(file: Path) -> Config:
    """
    Loads config pointed by the file variable

    Args:
        file (Path): An Path object to the desired config file

    Returns:
        Config: Instance of Config class containing loaded config
    """
    # Empty file path exception
    if(not file.exists()):
        raise(FileNotFoundError)

    config_return: Config = Config()

    # Load JSON file to a string
    raw_json: str = loadJSONtext(file)

    # Try to Parse JSON file
    try:
        json_object: dict = json.loads(raw_json)
    except json.JSONDecodeError:
        raise RuntimeError(f'Invalid JSON: {file}')

    # Read and save all properties that intrest us
    for value in Config.properties:
        try:
            setattr(config_return, value, json_object[value])
        except KeyError:
            pass

    return config_return


def loadJSONtext(file: Path) -> str:
    """
    Loads JSON file to a string 

    Args:
        file (Path): Path object pointing to a JSON file

    Returns:
        str: A string representation of a file
    """
    # Checks if file exist
    if(not file.exists()):
        raise(FileNotFoundError)

    with open(file, 'rt') as f:
        string_json: str = f.read()

    return string_json
