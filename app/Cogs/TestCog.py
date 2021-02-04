# Just for testing

#########################################################################################
# Library includes

from discord.ext import commands
from discord.ext.commands.context import Context
#########################################################################################
# App includes

from app.core import BotRuntime, getRuntime, BotClient
#########################################################################################


class TestCog(commands.Cog):

    def __init__(self, client: BotClient):
        self.client: BotClient = client
        self.runtime: BotRuntime = client.runtime
        self.log = self.runtime.log

    @commands.command()
    @commands.guild_only()
    async def echo(self, ctx: Context, *args):
        self.log.debug('Executing echo command')
        self.log.debug(f'Context is: {ctx.__dict__}')
        self.log.debug(f'Context type is {type(ctx)}')
        self.log.debug(f'Context message: {ctx.args}')
        self.log.debug(f'data is: {args}\n data type is{type(args)}')
        await ctx.message.reply("Hi")


def setup(client):
    client.add_cog(TestCog(client))
