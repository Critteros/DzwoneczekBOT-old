# This file will load tokens from .files

# Library includes
#########################################################################################
import pathlib
#########################################################################################
# App includes

# Types
from app.Types import configClass
#########################################################################################


def loadDiscordToken(*,
                     app_configuration: configClass.Config
                     ) -> str:
    """
    Loads discord token from given file and returns it as a string
    Args:
        app_configuration (configClass.Config): App configuration

    Raises:
        FileNotFoundError: Raises error if the token file does not exist

    Returns:
        str: Token representation as a string
    """

    # Set the file pointer to file from user defined config
    file: pathlib.Path = app_configuration.discord_token_file

    # Check if file exist and if not use the default file location
    if (not file.exists()):
        file = app_configuration.defaultConfig['discord_token_file']

    # If the file still does not exist than raise an FileNotFound error
    try:
        assert(file.exists())
    except AssertionError:
        raise FileNotFoundError('Cannot found discord token file')

    # Read the token
    with open(file, 'rt') as f:
        token_string: str = f.read()

    return token_string
