# Just for testing

#########################################################################################
# Library includes

from discord.ext import commands
from discord.ext.commands.context import Context
#########################################################################################
# App includes

from app.core import BotRuntime, getRuntime, BotClient

# Data Model
import app.DataModel as DataModel

# Logger
from app.Logging.LoggerCore import Logger
#########################################################################################


class AdminCommands(commands.Cog):

    def __init__(self, client: BotClient):
        self.client: BotClient = client
        self.runtime: BotRuntime = client.runtime
        self.log: Logger = self.runtime.log
        self.data_model: DataModel.Data = self.runtime.data_model

    @commands.group(name='prefix', hidden=True)
    @commands.guild_only()
    async def prefix_core(self, context: commands.Context):
        """
        Main handler for the prefix command

        Args:
            context (commands.Context): context of the invocation
        """
        if context.invoked_subcommand is None:
            await context.reply('Invalid Subcommand')

    @prefix_core.command(name='set', hidden=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def prefix_change(self, context: commands.Context, new_prefix: str):
        """
        Changes the current server command prefix

        Args:
            context (commands.Context): context of invocation
            new_prefix (str): the new prefix to be set
        """
        guild_id: int = context.guild.id
        self.log.info(
            f'Changing prefix in guild "{context.guild.name} to "{new_prefix}"')

        server_data: dict = self.data_model.get(guild_id, {})
        server_data['command_prefix'] = new_prefix

        await self.data_model.put(guild_id, server_data)
        await context.send(f'Changed server prefix to "{new_prefix}"')

    @prefix_core.command(name='current', hidden=True)
    @commands.guild_only()
    async def prefix_current(self, context: commands.Context):
        """
        Retrives the current prefix

        Args:
            context (commands.Context): context of the invocation
        """
        curr_prefix: str = (await self.client.get_prefix(context))[2]
        await context.send(f'Current prefix is set to "{curr_prefix}"')


def setup(client):
    client.add_cog(AdminCommands(client))
