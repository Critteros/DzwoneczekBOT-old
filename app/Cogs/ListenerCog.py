# Just for testing

#########################################################################################
# Library includes

from discord.ext import commands
#########################################################################################
# App includes

from app.core import BotRuntime, getRuntime, BotClient
#########################################################################################


class ListenerCog(commands.Cog):

    def __init__(self, client: BotClient):
        self.client: BotClient = client
        self.runtime: BotRuntime = client.runtime
        self.log = self.runtime.log

    @commands.Cog.listener()
    async def on_ready(self):
        self.runtime.log.info('Bot is ready')

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """
        Listener to handle error caused by improper use of bot commands

        Args:
            ctx (commands.Context): context that invoked error
            error (commands.CommandError): error that was invoked
        """

        # Check for error caused by DM bot directly with forbitted command
        if(isinstance(error, commands.NoPrivateMessage)):
            self.log.warning(
                f'User: "{ctx.author.name}" id:{ctx.author.id} attempted to use command "{ctx.command}" in private DM which is not permitted')
            await ctx.reply(f'Command "{ctx.command}" cannot be used in a private message. Sorry :(')

        if(isinstance(error, commands.MissingPermissions)):
            self.log.warning(
                f'User: "{ctx.author.name}" id:{ctx.author.id} attempted to use command "{ctx.command}" without needed permissions')
            await ctx.reply('You need Admin permissions to use that command')


def setup(client):
    client.add_cog(ListenerCog(client))
