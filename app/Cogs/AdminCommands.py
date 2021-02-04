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
#########################################################################################


class AdminCommands(commands.Cog):

    def __init__(self, client: BotClient):
        self.client: BotClient = client
        self.runtime: BotRuntime = client.runtime
        self.log = self.runtime.log


def setup(client):
    client.add_cog(AdminCommands(client))
