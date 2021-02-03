"""
This file is the entrypoint of Bot application
"""
#########################################################################################
# Library Includes

from pathlib import Path
#########################################################################################
# App includes


# /NEW

# Types
from app.Types import configClass
import app.Logging.LoggerCore as LoggerCore

# StartupTasks
from app.StartupTasks import configHandler
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
    """
    print("Starting up!")

    # Used variables and theri explenation
    app_configuration: configClass.Config  # Holds retrived app configuration
    app_logger: LoggerCore.Logger  # Holds reference to app logging system

    # Step one: load data from configs
    app_configuration = configHandler.getConfiguration(
        default_config_path=default_config_path,
        config_path=config_path
    )

    # Step two: Setup loggers
    logger_context: LoggerCore.Logger = LoggerCore.Logger(
        app_configuration=app_configuration
    )
    logger_context.debug('Logging is now available')

    # Listing app configuration
    logger_context.info('Listing app configuration')
    for key, value in app_configuration.__dict__.items():
        logger_context.info(f'\t{key}: {value}')
    logger_context.info('End of configuration')

    # Step three: load all tokens


    # # Load discord token
    # TokenLoader.loadDiscordToken()
    # # Init Runtime and attach it to globals
    # globals.runtime = BotRuntime(
    #     logger=globals.app_logger,
    #     client=BotClient(
    #         command_prefix=globals.app_configuration.command_prefix,
    #         logger=globals.app_logger
    #     ),
    #     configuration=globals.app_configuration,
    #     discord_token=globals.DISCORD_TOKEN
    # )
    # # Run bot
    # globals.runtime.run()
if __name__ != '__main__':
    print("Wrong file was run!\nRun file 'startup.py' instead")
else:
    main()
