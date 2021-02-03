# This file contains config class type to be imported in other modules for type hints

# Library includes
#########################################################################################
from typing import List
#########################################################################################


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
        'library_logging_type',
        'command_prefix'
    ]

    defaultConfig: dict = {}
