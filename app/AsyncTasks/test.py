# Just a test file for debbuging

#########################################################################################
# Library includes
import asyncio

#########################################################################################
# App includes

from app.core import BotRuntime, getRuntime
#########################################################################################


@BotRuntime.newStartupTask('Background Task')
async def test(string):
    runtime: BotRuntime = getRuntime()
    while True:
        runtime.log.warning(f'{string}')
        await asyncio.sleep(5)
