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
import app.Types as Types
import app.Logging.LoggerCore as LoggerCore

# StartupTasks
import app.StartupTasks as StartupTasks
#########################################################################################

# Paths constants
default_config_path: Path = Path('./app/default_config.json')
config_path: Path = Path('./config.json')


def main() -> None:
    """
    Quick summary of how application starts:
    1) Configs are loaded from JSONs and parsed 
    """
    print("Starting up!")

    # Used variables and theri explenation
    app_configuration: Types.configClass.Config  # Holds retrived app configuration
    app_logger: LoggerCore.Logger  # Holds reference to app logging system

    # Step one load data from configs
    app_configuration = StartupTasks.config_handler.getConfiguration()

    # # Load Configuration from JSONs
    # globals.app_configuration: Config = getConfiguration(
    #     default_config_path=default_config_path,
    #     config_path=config_path
    # )

    # # Retrive loggers
    # globals.app_logger = Logger(globals.app_configuration)
    # globals.app_logger.debug('Finished initializing loggers')

    # # Listing configuration
    # globals.app_logger.info('Listing Configuration:')
    # for key, value in globals.app_configuration.__dict__.items():
    #     globals.app_logger.info(f'\t{key}: {value}')
    # globals.app_logger.info('End of configuration')
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
