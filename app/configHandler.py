# Note: This file excecutes it's code before Logging systems are loader thus logging is not possible in this file

# Library includes
import json
from typing import List
from pathlib import Path

# App includes
from app.Logging.LoggingGlobals import levels, console_types, logging_types
from app.Globals import default_config_path, config_path


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

    _validateConfig(configuration)
    return configuration


def _validateConfig(config: Config) -> None:
    """
    Validates config file and changes values in the config if they are out of defined range to default values. For internal use only

    Args:
        config (Config): The config file to validate
    """
    # Defaults
    defaults: dict = Config.defaultConfig

    # Log to Console
    specified_obj = config.log_to_console
    if(not isinstance(specified_obj, bool)):
        config.log_to_console = defaults['log_to_console']

    # Log to file
    specified_obj = config.log_to_file
    if(not isinstance(specified_obj, bool)):
        config.log_to_file = defaults['log_to_file']

    # Log library
    specified_obj = config.log_library
    if(not isinstance(specified_obj, bool)):
        config.log_library = defaults['log_library']

    # Console Log level
    specified_level = config.console_log_level
    if(specified_level not in levels):
        config.console_log_level = defaults['console_log_level']

    # File Log Level
    specified_level = config.file_log_level
    if(specified_level not in levels):
        config.file_log_level = defaults['file_log_level']

    # Library Log Level
    specified_level = config.library_log_level
    if(specified_level not in levels):
        config.library_log_level = defaults['library_log_level']

    # Console logger type
    specified_type = config.console_logger_type
    if(specified_type not in console_types):
        config.console_logger_type = defaults['console_logger_type']

    # Library logging type
    specified_type = config.library_logging_type
    if(specified_type not in logging_types):
        config.library_logging_type = defaults['library_logging_type']


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
