# File that holds main Runtime class and can be included in every file in project without problems with imports

# Library includes
#########################################################################################
import asyncio
from types import CoroutineType
#########################################################################################
# App includes


# Include types
from app.Types import configClass
from app.Logging import LoggerCore

# Bot client
from app.BotClient import BotClient

#########################################################################################


class BotRuntime:
    """
        Main Runtime class that contain critical information about app execution
    """
    # Class stuff
    #########################################################################################

    # Container for tasks
    app_tasks: list = []

    # Decorators
    # If you do not know how decorators work than skip this part it's called magic
    #########################################################################################

    @classmethod
    def newTask(cls, *args, **kwargs):
        """
            Decorator for adding a coroutine to an event loop

            In more technical point of view this is decorator primer which primes the decorator() function.
            decorator() function than decorates given function using it's wrapper() function
        """

        # Don't even try to understand this magic
        def decorator(function: CoroutineType):
            """
                Main decorator which decorates async function
            Args:
                function (CoroutineType): [description]
            """

            async def wrapper(*args, **kwargs):
                """
                    Wrapper around passed function
                """
                # Make sure that bot has connected to discord before doing anything
                await (getRuntime().client.wait_until_ready())
                # Original function
                await function(*args, **kwargs)

            # Append to queque courutine call
            cls.app_tasks.append(wrapper(*args, **kwargs))

            # Return decorated function
            return wrapper

        # Return main decorator from primer decorator
        return decorator

    # Instance stuff
    #########################################################################################
    def __init__(self, *,
                 configuration: configClass.Config,
                 logger: LoggerCore.Logger,
                 discord_token: str
                 ):
        """
        This initiates the BotRuntime and saves information abot current running application, there should be only one instance of this class!
        Instance after initialisation is saved to currentRuntime variable in this module, getRuntime() returns current runtime object

        Args:
            configuration (configClass.Config): App configuration object
            logger (LoggerCore.Logger): App logger instance
            discord_token (str): Discord API key

        Returns:
            BotRuntime: Initialisated Runtime
        """
        logger.debug('Initializing BotRuntime instance')

        # Attach info about Runtime
        #########################################################################################
        logger.debug('Attaching logger')
        self.log: LoggerCore.Logger = logger

        logger.debug('Attaching event-loop')
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        logger.debug('Attaching bot-configuration')
        self.configuration: configClass.Config = configuration

        logger.debug('Attaching discord token')
        self.discord_token: str = discord_token
        #########################################################################################
        # Setting up client

        logger.debug('Setting up BotClient')
        self.client: BotClient = BotClient(
            command_prefix=configuration.discord_token_file,
            logger=logger,
            discord_token=discord_token
        )
        #########################################################################################
        # Setting up tasks to run
        logger.debug('Setting up task to be run in event loop')

        # Cleanup Tasks
        self.cleanupTasks: list = [
            self.client.logout()
        ]

        # Startup Tasks
        self.start_tasks: list = [

        ]

        #########################################################################################
        # Scheduing tasks
        logger.debug('Scheduing tasks')
        self.activeTasks: list = []
        self.discordClientTask: asyncio.Task = None

        logger.debug('Scheduing discord client task')
        self.discordClientTask = self.loop.create_task(
            self.client.start(self.discord_token))

        for corutine in self.start_tasks:
            task: asyncio.Task = self.loop.create_task(corutine)
            self.activeTasks.append(task)
        logger.debug('Done scheduing tasks')
        logger.debug(self.activeTasks)

        # Test
        for corutine in BotRuntime.app_tasks:
            task: asyncio.Task = self.loop.create_task(corutine)
            self.activeTasks.append(task)

        #########################################################################################
        logger.debug('End of Runtime initialization')
        global currentRuntime
        currentRuntime = self
        self.client.command()

    def run(self):
        try:
            self.log.info('Running event loop')
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.log.warning('Recived KeyboardInterrupt shutting down')
            self.loop.run_until_complete(self.cleanup())
        finally:
            self.log.warning('Closing event loop')
            self.loop.close()

    async def cleanup(self) -> None:
        """
        Function to clean up the event loop
        """
        self.log.debug('Cleaning up event loop')
        cleanup_tasks = self.cleanupTasks

        for task in cleanup_tasks:
            self.log.debug(f'Awaiting task: {task}')
            await task

        self.log.debug('Closing app running tasks')
        for task in self.activeTasks:
            self.log.debug(f'Closing task {task}')
            task.cancel()


# A container for the current runtime
currentRuntime: BotRuntime = None


def getRuntime() -> BotRuntime:
    """
    This function is getter for the current runtime object

    Returns:
    BotRuntime: Current runtime
    """
    global currentRuntime
    return currentRuntime


@BotRuntime.newTask('abba')
async def test(string):
    runtime: BotRuntime = getRuntime()
    while True:
        runtime.log.error(f'Value: {string}')
        await asyncio.sleep(3)
