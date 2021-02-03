# This file will load tokens from .files

# Library includes
#########################################################################################
import pathlib
#########################################################################################
# App includes

#########################################################################################


def loadDiscordToken() -> None:
    """
    Loads discord token string from file specfied in config entry 'discord_token_file'

    Args:
        config (Config): App configuration
    """
    globals.app_logger.debug('Preparing to load discord token')
    file_path: Path = Path(globals.app_configuration.discord_token_file)
    # Check if file exist
    if (not file_path.exists()):
        file_path: Path = Path(
            globals.app_configuration.defaultConfig.discord_token_file)

    try:
        assert(file_path.exists())
    except AssertionError:
        globals.app_logger.critical('Discord token file cannot be found')
        raise RuntimeError('Cannot found discord token file')

    with open(file_path, 'rt') as f:
        token_string: str = f.read()

    globals.app_logger.debug(f'Read token string from file {file_path}')
    #globals.app_logger.debug(f'Token was: /{token_string}/')
    globals.DISCORD_TOKEN = token_string
