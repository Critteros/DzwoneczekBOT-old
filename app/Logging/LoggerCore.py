
# Library includes
import logging
import coloredlogs
import os

from sys import stdout
from typing import Dict, List


# App includes
import app.Logging.styles as styles

from app.configHandler import Config
from app.Logging.LoggingGlobals import levels, console_types, logging_types


class Logger:
    """
    Main abstraction for group of multiple Loggers and logging methods.
    There should be only one instance of this class in an running Application,
    multiple instances may cause undefined behavior.
    """

    def __init__(self, _configuration: Config):

        # Change instance to dict format
        configuration: dict = _configuration.__dict__

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
            'console': None,
            'file': None
        }
        self.aciveLibraryLogger = None

        # Activate Loggers
        if(self.consoleLogger):
            _activateConsole(self)
        if(self.fileLogger):
            _activateFile(self)
        if(self.libraryLogger):
            _activateLibrary(self)

    def debug(self, *args, **kwargs):
        """
        Prints debug level message in active loggers
        """
        for activeLogger in self.activeLoggers.values():
            if activeLogger is not None:
                activeLogger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        """
        Prints info level message in active loggers
        """
        for activeLogger in self.activeLoggers.values():
            if activeLogger is not None:
                activeLogger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        """
        Prints warning level message in active loggers
        """
        for activeLogger in self.activeLoggers.values():
            if activeLogger is not None:
                activeLogger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        """
        Prints error level message in active loggers
        """
        for activeLogger in self.activeLoggers.values():
            if activeLogger is not None:
                activeLogger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        """
        Prints critical level message in active loggers
        """
        for activeLogger in self.activeLoggers.values():
            if activeLogger is not None:
                activeLogger.critical(*args, **kwargs)


def _activateConsole(context: Logger) -> None:
    """
    Activates and configures the console logger.
    For internal use only

    Args:
        context (Logger): Containment for loggers
    """
    # Setup
    logging_level: int = levels[context.consoleLevel]
    logging_type: str = context.consoleType
    useColor: bool = True if context.consoleType == 'color' else False

    logging_instance: logging.Logger = logging.getLogger('BotConsole')
    logging_instance.setLevel(logging_level)

    if(useColor):
        coloredlogs.install(
            level=logging_level,
            fmt=styles.logging_format,
            level_styles=styles.level_style,
            field_styles=styles.field_style,
            logger=logging_instance,
            stream=stdout
        )
    else:
        # Create STDOUT handler
        handler = logging.StreamHandler(stdout)
        handler.setLevel(logging_level)

        # Create formatter
        formater = logging.Formatter(
            fmt=styles.logging_format, datefmt='%Y-%m-%d %H:%M:%S')

        # Attach formater
        handler.setFormatter(formater)

        # Attach handler
        logging_instance.addHandler(handler)

    context.activeLoggers['console'] = logging_instance


def _activateFile(context: Logger) -> None:
    """
    Activates and configures the file logger.
    For internal use only

    Args:
        context (Logger): Containment for loggers
    """
    # Setup
    logging_level: int = levels[context.fileLevel]

    # Try to make a Logs directory if one does not exist
    try:
        os.mkdir('Logs')
    except OSError:
        pass

    logging_instance: logging.Logger = logging.getLogger('BotFile')
    logging_instance.setLevel(logging_level)

    # Handler
    handler: logging.FileHandler = logging.FileHandler('Logs/bot.log')
    handler.setLevel(logging_level)

    # Formatter
    formatter: logging.Formatter = logging.Formatter(
        fmt=styles.logging_format,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler.setFormatter(formatter)
    logging_instance.addHandler(handler)
    context.activeLoggers['file'] = logging_instance


def _activateLibrary(context: Logger) -> None:
    """
    Activates and configures the library logger.
    For internal use only

    Args:
        context (Logger): Containment for loggers
    """
    # Setup
    logging_level: int = levels[context.libraryLevel]

    # Try to make a Logs directory if one does not exist
    try:
        os.mkdir('Logs')
    except OSError:
        pass

    logging_instance: logging.Logger = logging.getLogger('discord')
    logging_instance.setLevel(logging_level)

    # Handler
    handler: logging.FileHandler = logging.FileHandler(
        'Logs/internal-discord.log')
    handler.setLevel(logging_level)

    # Formatter
    formatter: logging.Formatter = logging.Formatter(
        fmt=styles.logging_format,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler.setFormatter(formatter)
    logging_instance.addHandler(handler)
    context.aciveLibraryLogger = logging_instance
