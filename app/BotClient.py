# This file contains main Bot Client used for communication with discord API

# Library includes
#########################################################################################
from discord.ext import commands
#########################################################################################
# App includes

from app.Logging import LoggerCore
#########################################################################################


class BotClient(commands.Bot):
    def __init__(self, *,
                 command_prefix: str,
                 logger: LoggerCore.Logger,
                 discord_token: str
                 ):
        """
        This is app subclass of command.Bot client

        Args:
            command_prefix (str): Command prefix to be used by the bot
            logger (LoggerCore.Logger): Bot Logger
            discord_token (str): Discord token as a string

        Returns:
            BotClient instance
        """
        # Calling super class constructor
        logger.debug(
            f'Calling commands.Bot constructor with prefix: {command_prefix}')
        super().__init__(command_prefix=command_prefix)

        # Attaching client properties
        logger.debug('Attching BotClient properties')
        self.app_logger: LoggerCore.Logger = logger
        self.discord_token: str = discord_token

        logger.debug('End of BotClient initialization')

    async def on_ready(self):
        self.app_logger.info('Bot is ready!')
