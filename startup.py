"""
This file is the entrypoint of Bot application
"""
#########################################################################################
# Library Includes

from pathlib import Path
#########################################################################################
# App includes

# Types
from app.Types import configClass
import app.Logging.LoggerCore as LoggerCore

# StartupTasks
from app.StartupTasks import configHandler, TokenLoader

# Importing core
import app.core as core

# Logging Banners
import app.Logging.Banners.LoggingBanners as Banners

# Import Data Model
import app.DataModel as DataModel

#########################################################################################
# Task primer
from app.AsyncTasks import *
#########################################################################################

# Paths constants
default_config_path: Path = Path('./app/default_config.json')
config_path: Path = Path('./config.json')


def main() -> None:
    """
    Quick summary of how application starts:
    1) Configs are loaded from JSONs and parsed
    2) Setup Loggers  
    3)Load all needed tokens
    4)Initialize Data Model
    5)Create BotRuntime instance
    6)Startup bot
    """
    print("Starting up!")

    # Used variables and theri explenation
    app_configuration: configClass.Config  # Holds retrived app configuration
    app_logger: LoggerCore.Logger          # Holds reference to app logging system
    DISCORD_TOKEN: str                     # Discord API token used for communication
    data_model: DataModel.Data             # Data model used in the application

    # Step one: load data from configs
    app_configuration = configHandler.getConfiguration(
        default_config_path=default_config_path,
        config_path=config_path
    )

    #########################################################################################
    # Step two: Setup loggers

    logger_context: LoggerCore.Logger = LoggerCore.Logger(
        app_configuration=app_configuration
    )
    logger_context.info('Logging is now available')
    logger_context.info(Banners.setup_phaze)

    # Listing app configuration
    logger_context.info(Banners.config)
    logger_context.warning('Listing app configuration')
    for key, value in app_configuration.__dict__.items():
        logger_context.info(f'\t-> {key}: {value}')
    logger_context.warning('End of configuration')
    logger_context.info(Banners.config)

    logger_context.info('End of setup phaze two: Setting up Loggers')
    #########################################################################################
    # Step three: load all tokens
    logger_context.info('Setup phaze three: Loading tokens')

    # Load discord token
    logger_context.info('Loading discord token')
    DISCORD_TOKEN = TokenLoader.loadDiscordToken(
        app_configuration=app_configuration)
    logger_context.info('Discord token file was loaded')

    logger_context.info('End of setup phaze three: Loading tokens')
    #########################################################################################
    # Step four: Create Data Model
    logger_context.info('Setup phaze four: Create Data Model')

    data_model = DataModel.Data()

    logger_context.info('End of phaze four: Create Data Model')
    #########################################################################################
    # Step five: Create BotRuntime instance
    logger_context.info('Setup phaze five: Creating BotRuntime')
    core.BotRuntime(
        configuration=app_configuration,
        logger=logger_context,
        discord_token=DISCORD_TOKEN,
        data_model=data_model
    )
    logger_context.info('End of phaze five: Creating BotRuntime')
    #########################################################################################
    # Step six: Startup bot
    logger_context.info('Setup phaze six: Startup bot')
    core.getRuntime().run()


if __name__ != '__main__':
    print("Wrong file was run!\nRun file 'startup.py' instead")
else:
    main()
