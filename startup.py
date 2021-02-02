
# Library includes
from pathlib import Path


# App includes
import app.configHandler as configHandler
from app.Logging.LoggerCore import Logger


def main() -> None:
    print("Starting up!")

    # Load Configuration from JSONs
    BotConfiguration: configHandler.Config = configHandler.getConfiguration()

    # Retrive loggers
    logger: Logger = Logger(BotConfiguration)
    logger.debug('Finished initializing loggers')

    # Listing configuration
    logger.info('Listing Configuration:')
    for key, value in BotConfiguration.__dict__.items():
        logger.info(f'\t{key}: {value}')
    logger.info('End of configuration')


if __name__ != '__main__':
    print("Wrong file was run!\nRun file 'startup.py' instead")
else:
    main()
