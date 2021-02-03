# This file contains main Bot Client used for communication with discord API

# Library includes
#########################################################################################
from discord.ext import commands
#########################################################################################

# App includes
#########################################################################################

# Include Globals
from app.Globals import globals
#########################################################################################


class BotClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=globals.app_configuration.command_prefix)

    async def on_ready(self):
        globals.app_logger.info('Bot is ready!')
