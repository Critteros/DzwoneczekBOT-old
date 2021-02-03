# This file contains all Global variables use through program lifecycle
# this file only contains definitions of variables and will not execute any code

# Library includes
#########################################################################################
from pathlib import Path
#########################################################################################


# Type includes
#########################################################################################

# Include Logger type for typing info
from app.Logging.LoggerCore import Logger

# Include Config type for typing ingo
from app.configClass import Config

# Include core
from app.core import BotRuntime

#########################################################################################


class globals:
    # Utility classes
    app_logger: Logger = None
    app_configuration: Config = None
    runtime: BotRuntime = None

    # Tokens
    DISCORD_TOKEN: str = ''


# Paths
default_config_path: Path = Path('./app/default_config.json')
config_path: Path = Path('./config.json')
