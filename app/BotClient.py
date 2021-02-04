# This file contains main Bot Client used for communication with discord API

# Library includes
#########################################################################################
from discord.ext import commands
import pathlib
import discord
#########################################################################################
# App includes

from app.Logging import LoggerCore

# Data Model
import app.DataModel as DataModel
#########################################################################################


# Function that retrives command prefix
def _getPrefix(default_prefix: str):
    def wrapper(bot: BotClient, msg: discord.Message):
        bot_user_id = bot.user.id
        prefixes: list = [f'<@!{bot_user_id}> ', f'<@{bot_user_id} ']

        if msg.guild is None:
            prefixes.append('!')
            prefixes.append('?')
        else:
            guild_id: int = msg.guild.id
            prefixes.extend(bot.data_model.get(guild_id, [default_prefix]))

        return prefixes
    return wrapper


class BotClient(commands.Bot):
    def __init__(self, *,
                 command_prefix: str,
                 logger: LoggerCore.Logger,
                 discord_token: str,
                 runtime,
                 data_model: DataModel.Data
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
        # logger.debug(f'Calling commands.Bot constructor with prefix: /{command_prefix}/')
        super().__init__(
            command_prefix=_getPrefix(command_prefix)
        )

        # Attaching client properties
        logger.debug('Attching BotClient properties')
        self.app_logger: LoggerCore.Logger = logger
        self.discord_token: str = discord_token
        self.runtime = runtime
        self.data_model = data_model

        # Loading cogs
        self.app_logger.info('Loading cogs')
        cogs_dir: str = './app/Cogs/'
        directory: pathlib.Path = pathlib.Path(cogs_dir)

        for file in directory.iterdir():
            file_name: str = file.name

            if (file_name.endswith('.py')):
                cog_name: str = f'app.Cogs.{file_name[:-3]}'
                self.app_logger.info(f'Adding Cog: {cog_name}')
                self.load_extension(cog_name)

        self.app_logger.info('Finished loading cogs')

        logger.debug('End of BotClient initialization')

    # async def on_ready(self):
    #     self.app_logger.info('Bot is ready!')
