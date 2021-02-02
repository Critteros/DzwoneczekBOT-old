import json
from typing import List
from pathlib import Path

# Configuration global variables
default_config_path: Path = Path('./app/default_config.json')
config_path: Path = Path('./config.json')


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
        'discord_token_file',
        'library_logging_type'
    ]

    defaultConfig: dict = {}


def getConfiguration() -> Config:
    """
    Function that reads and compiles bot configuration
    Returns:
        Config: Bot configuration as an instance of a class
    """
    # Value to be returned
    configuration: Config = Config()

    # Check if default configuration file exist
    if(not default_config_path.exists()):
        raise(FileNotFoundError('Default Configuration File was not found!'))

    # Check if user configuration file exist, if not than create one from default configuration
    if(not config_path.exists()):
        # Creates confguration from default config file
        _createConfiguration()

    # Compile the configuration file
    user_configuration: Config = loadConfig(config_path)
    default_configuration: Config = loadConfig(default_config_path)

    Config.defaultConfig = default_configuration.__dict__

    for _property in Config.properties:
        if (hasattr(user_configuration, _property)):
            setattr(configuration, _property,
                    user_configuration.__dict__[_property])
        else:
            setattr(configuration, _property,
                    default_configuration.__dict__[_property])
    return configuration


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


def _createConfiguration() -> None:
    """
    Creates user-config file based on the default_config.json
    Intended for internal use only
    """
    # Read the Default Configuration file
    with open(default_config_path, "rt") as default:
        default_data: str = default.read()

    # Create config file
    assert(not config_path.exists())
    with open(config_path, "wt") as f:
        f.write(default_data)
