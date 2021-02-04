# Just for testing

#########################################################################################
# Library includes

from discord.ext import commands
#########################################################################################
# App includes

from app.core import BotRuntime, getRuntime, BotClient
#########################################################################################


class TestCog(commands.Cog):

    def __init__(self, client: BotClient):
        self.client: BotClient = client
        self.runtime: BotRuntime = client.runtime

    @commands.Cog.listener()
    async def on_ready(self):
        self.runtime.log.info('Bot is ready')
        self.runtime.log.debug(self.runtime.__dict__)


def setup(client):
    client.add_cog(TestCog(client))
