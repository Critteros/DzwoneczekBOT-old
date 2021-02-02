from pathlib import Path


# App includes
import app.configHandler as configHandler

# For testing only
from app.configHandler import default_config_path, config_path


def main() -> None:
    print("Starting up!")

    BotConfiguration: configHandler.Config = configHandler.getConfiguration()
    print(BotConfiguration.__dict__)


if __name__ != '__main__':
    print("Wrong file was run!\nRun file 'startup.py' instead")
else:
    main()
