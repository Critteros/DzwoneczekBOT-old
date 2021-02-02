from pathlib import Path

# App includes
from app.configHandler import loadConfig


def main() -> None:
    print("Hello World")

    # Loding config paths
    default_config_path: Path = Path('./app/default_config.json')
    config_path: Path = Path('./config.json')

    if(not default_config_path.exists()):
        print("Default Config File not found!")
        raise(FileNotFoundError)
    if(not config_path.exists()):
        print("Config File not found!")
        raise(FileNotFoundError)

    print(loadConfig(default_config_path).__dict__)


if __name__ != '__main__':
    print("Wrong file was run!\nRun file 'startup.py' instead")
else:
    main()
