# This file contains main Bot Client used for communication with discord API

# Library includes
#########################################################################################
from discord.ext import commands
#########################################################################################

# App includes
#########################################################################################
from app.Logging.LoggerCore import Logger
#########################################################################################


class BotClient(commands.Bot):
    def __init__(self, *, command_prefix: str, logger: Logger):
        super().__init__(command_prefix=command_prefix)
        self.app_logger = logger

    async def on_ready(self):
        self.app_logger.info('Bot is ready!')
