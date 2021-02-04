# File that holds main Runtime class and can be included in every file in project without problems with imports

# Library includes
#########################################################################################
import asyncio
from types import CoroutineType

# Data structures
import queue
#########################################################################################
# App includes

# Include types
from app.Types import configClass
from app.Logging import LoggerCore

# Bot client
from app.BotClient import BotClient

# Banners
import app.Logging.Banners.LoggingBanners as Banners

#########################################################################################


class BotRuntime:
    """
        Main Runtime class that contain critical information about app execution
    """
    # Class stuff
    #########################################################################################

    # Container for app coroutines
    app_coroutines: queue.Queue = queue.Queue()
    cleanup_coroutines: queue.Queue = queue.Queue()

    # Decorators
    # If you do not know how decorators work than skip this part it's called magic
    #########################################################################################

    @classmethod
    def newStartupTask(cls, *args, **kwargs):
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
            cls.app_coroutines.put(wrapper(*args, **kwargs))

            # Return decorated function
            return wrapper

        # Return main decorator from primer decorator
        return decorator

    @classmethod
    def newCleanupTask(cls, *args, **kwargs):
        """
            Decorator for adding a cleanup coroutine to an event loop cleanup process

            In more technical point of view this is decorator primer which primes the decorator() function.
            decorator() function than decorates given function using it's wrapper() function
        """

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
            cls.cleanup_coroutines.put(wrapper(*args, **kwargs))

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
        logger.info('Initializing BotRuntime instance')

        # Attach info about Runtime
        #########################################################################################
        logger.info('Attaching logger to runtime')
        self.log: LoggerCore.Logger = logger

        logger.info('Attaching event-loop to runtime')
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        logger.info('Attaching bot-configuration to runtime')
        self.configuration: configClass.Config = configuration

        logger.info('Attaching discord token to runtime')
        self.discord_token: str = discord_token

        logger.info('Creating task queque object')
        self.task_queue: queue.Queue = queue.Queue()
        #########################################################################################
        # Setting up the client

        logger.info('Setting up BotClient')
        self.client: BotClient = BotClient(
            command_prefix=configuration.discord_token_file,
            logger=logger,
            discord_token=discord_token
        )
        logger.info('Done setting up Discord Client')
        #########################################################################################
        # Loading cogs

        #########################################################################################
        # Scheduing tasks

        # Scheduing discord API run
        logger.info('Scheduling main discord client task')
        self.loop.create_task(self.client.start(self.discord_token))
        logger.info('Done scheduling discord client task')

        # Heping variables
        to_schedue: queue.Queue = BotRuntime.app_coroutines
        loop = self.loop

        logger.info('Scheduling StartupTasks from decorator')
        while(not to_schedue.empty()):
            curr_coro: asyncio.Task = to_schedue.get()
            logger.debug(f'Scheduing task: {curr_coro}')
            self.task_queue.put(loop.create_task(curr_coro))

        logger.info('Done scheduing startup tasks')
        logger.debug(f'Task queque is: {self.task_queue}')

        #########################################################################################
        logger.info('End of Runtime initialization')
        global currentRuntime
        currentRuntime = self

        # End of initialization
        #########################################################################################

    def run(self):
        try:
            self.log.info(Banners.end_of_setup)
            self.log.warning('Running event loop')
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

        # Helper variables
        cleanup_tasks = BotRuntime.cleanup_coroutines
        task_queque = self.task_queue
        logger = self.log

        logger.info('Cleaning up event loop')

        # Terminating all tasks
        logger.info('Closing all running tasks')
        while (not task_queque.empty()):
            curr_task: asyncio.Task = task_queque.get()
            logger.debug(f'Closing task: {curr_task}')
            curr_task.cancel()

        # Processing all cleanup coros
        logger.info('Processing all cleanup coros')
        while (not cleanup_tasks.empty()):
            curr_coro = cleanup_tasks.get()
            logger.debug(f'Processing cleanup_coro: {curr_coro}')
            await curr_coro

        # Logging out of discord API
        logger.warning('Logging out of discord')
        await self.client.logout()

        logger.info('Finished Cleanup!')


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
