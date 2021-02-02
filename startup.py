from pathlib import Path


# App includes
import app.configHandler as configHandler
from app.Logging.LoggerCore import Logger

# For testing only
from app.configHandler import default_config_path, config_path


def main() -> None:
    print("Starting up!")

    BotConfiguration: configHandler.Config = configHandler.getConfiguration()
    print(BotConfiguration.__dict__)
    # Logger(BotConfiguration)


if __name__ != '__main__':
    print("Wrong file was run!\nRun file 'startup.py' instead")
else:
    main()
