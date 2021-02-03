# File that holds main Runtime class

# Library includes
#########################################################################################
import asyncio
#########################################################################################

# App includes
#########################################################################################

# Include types
from app.BotClient import BotClient
from app.Logging.LoggerCore import Logger
from app.configClass import Config

#########################################################################################


class BotRuntime:
    def __init__(self, *,
                 logger: Logger,
                 client: BotClient,
                 configuration: Config,
                 discord_token: str
                 ):

        # Attach info about Runtime
        self.log = logger
        self.client = client
        self.loop = asyncio.get_event_loop()
        self.configuration = configuration
        self.discord_token = discord_token

    def run(self):
        try:
            self.loop.run_until_complete(self.client.start(self.discord_token))
        except KeyboardInterrupt:
            self.log.warning('Recived KeyboardInterrupt shutting down')
            self.loop.run_until_complete(self.client.logout())
        finally:
            self.log.info('Closing event loop')
            self.loop.close()
