from sys import stdout
from typing import Dict, List

# App includes
import app.Logging.styles as styles
from app.configHandler import Config

# Logging Globals
levels: Dict[str, int] = {'DEBUG': 10, 'INFO': 20,
                          'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}

console_types: List[str] = ['normal', 'color']
logging_types: List[str] = ['console', 'file']

# Main logging abstraction


class Logger:

    def __init__(self, configuration: Config):

        # Change instance to dict format
        configuration: dict = configuration.__dict__

        # What loggers should be activated
        self.consoleLogger: bool = configuration['log_to_console']
        self.fileLogger: bool = configuration['log_to_file']
        self.libraryLogger: bool = configuration['log_library']

        # Log levels
        self.consoleLevel: str = configuration['console_log_level']
        self.fileLevel: str = configuration['file_log_level']
        self.libraryLevel: str = configuration['library_log_level']

        # Special attributes
        self.consoleType: str = configuration['console_logger_type']
        self.libraryLoggingType: str = configuration['library_logging_type']

        # Loggers
        self.activeLoggers: Dict[any] = {
            'console': None, 'file': None, 'library': None}
