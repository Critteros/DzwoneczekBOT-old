# Note: This file excecutes it's code before Logging systems are loader thus logging is not possible in this file


#########################################################################################
# Library includes

import json
import pathlib
from typing import List
#########################################################################################
# App includes

# Types
from app.Types import configClass as configClass

# Predefined Logging Constants used to validate config files
from app.Logging.LoggingGlobals import levels, console_types, logging_types
#########################################################################################


def getConfiguration(*,
                     default_config_path: pathlib.Path,
                     config_path: pathlib.Path
                     ) -> configClass.Config:
    """
    Function that reads and compiles bot configuration
    Returns:

    Args:
        default_config_path (pathlib.Path): default configuration path 
        config_path (pathlib.Path): config path 

    Returns:
        configClass.Config: App configuration as a instance of Config class
    """

    # Value to be returned
    app_configuration: configClass.Config = configClass.Config()

    # Check if default configuration file exist
    if(not default_config_path.exists()):
        raise(FileNotFoundError('Default Configuration File was not found!'))

    # Check if user configuration file exist, if not than create one from default configuration
    if(not config_path.exists()):
        # Creates confguration from default config file
        _createConfiguration(
            default_config_path=default_config_path,
            config_path=config_path
        )

    # Read the configuration files
    user_configuration: configClass.Config = loadConfig(file_path=config_path)
    default_configuration: Config = loadConfig(file_path=default_config_path)

    # Bind default configuration to configClass.py
    configClass.Config.defaultConfig = default_configuration.__dict__

    # Take sum of two configs and combine them to one config file that will be returned
    for value in configClass.Config.properties:
        # Check if user specified configuration has specified property
        if (hasattr(user_configuration, value)):
            # If user specified has that property than append it to returned config
            setattr(
                app_configuration,
                value,
                user_configuration.__dict__[value]
            )

        else:
            # If not than append the default config's value
            setattr(
                app_configuration,
                value,
                default_configuration.__dict__[value]
            )

    # Mutatuve function that validates the app configuration
    _validateConfig(app_configuration)
    return app_configuration


def _validateConfig(config: configClass.Config) -> None:
    """
    Validates config file and changes values in the config if they are out of defined range to default values. For internal use only

    Args:
        config (configClass.Config): The config file to validate
    """
    # Defaults
    defaults: dict = configClass.Config.defaultConfig

    # Log to Console property
    specified_obj = config.log_to_console
    if(not isinstance(specified_obj, bool)):
        config.log_to_console = defaults['log_to_console']

    # Log to file property
    specified_obj = config.log_to_file
    if(not isinstance(specified_obj, bool)):
        config.log_to_file = defaults['log_to_file']

    # Log library property
    specified_obj = config.log_library
    if(not isinstance(specified_obj, bool)):
        config.log_library = defaults['log_library']

    # Console Log level property
    specified_level = config.console_log_level
    if(specified_level not in levels):
        config.console_log_level = defaults['console_log_level']

    # File Log Level property
    specified_level = config.file_log_level
    if(specified_level not in levels):
        config.file_log_level = defaults['file_log_level']

    # Library Log Level property
    specified_level = config.library_log_level
    if(specified_level not in levels):
        config.library_log_level = defaults['library_log_level']

    # Console logger type property
    specified_type = config.console_logger_type
    if(specified_type not in console_types):
        config.console_logger_type = defaults['console_logger_type']

    # Library logging type property
    specified_type = config.library_logging_type
    if(specified_type not in logging_types):
        config.library_logging_type = defaults['library_logging_type']


def loadConfig(*,
               file_path: pathlib.Path
               ) -> configClass.Config:
    """
    Loads config pointed by the file variable

    Args:
        file_path (pathlib.Path): Path object pointing to config file in JSON format

    Returns:
        configClass.Config: Instance of Config class containing loaded config
    """

    # Ckeck if file exists
    if(not file_path.exists()):
        raise(FileNotFoundError)

    # Config instance to be returned
    config_return: configClass.Config = configClass.Config()

    # Load JSON file to a string
    with open(file_path, 'rt') as f:
        raw_json: str = f.read()

    # Try to Parse JSON file
    try:
        json_object: dict = json.loads(raw_json)
    except json.JSONDecodeError:
        raise RuntimeError(f'Invalid JSON: {file_path}')

    # Read and save all properties that intrest us
    for value in configClass.Config.properties:
        try:
            setattr(config_return, value, json_object[value])
        except KeyError:
            pass

    return config_return


def _createConfiguration(*,
                         default_config_path: str,
                         config_path: str
                         ) -> None:
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
