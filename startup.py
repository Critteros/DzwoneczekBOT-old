
# Library includes
#########################################################################################
from pathlib import Path
#########################################################################################


# App includes
#########################################################################################

# Function to load configuration
from app.configHandler import getConfiguration

# TokenLoader module
import app.TokenLoader as TokenLoader

# Import Global variables
from app.Globals import globals

# Import for types
from app.configClass import Config
from app.Logging.LoggerCore import Logger

# BotClient
from app.BotClient import BotClient
#########################################################################################


def main() -> None:
    print("Starting up!")

    # Load Configuration from JSONs
    globals.app_configuration: Config = getConfiguration()

    # Retrive loggers
    globals.app_logger = Logger(globals.app_configuration)
    globals.app_logger.debug('Finished initializing loggers')

    # Listing configuration
    globals.app_logger.info('Listing Configuration:')
    for key, value in globals.app_configuration.__dict__.items():
        globals.app_logger.info(f'\t{key}: {value}')
    globals.app_logger.info('End of configuration')

    # Load discord token
    TokenLoader.loadDiscordToken()

    client: BotClient = BotClient()
    client.run(globals.DISCORD_TOKEN)


if __name__ != '__main__':
    print("Wrong file was run!\nRun file 'startup.py' instead")
else:
    main()
