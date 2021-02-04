# Just a test file for debbuging

#########################################################################################
# Library includes
import asyncio

#########################################################################################
# App includes

from app.core import BotRuntime, getRuntime
#########################################################################################


@BotRuntime.newStartupTask('lalalal')
async def test(string):
    runtime: BotRuntime = getRuntime()
    while True:
        runtime.log.error(f'Value: {string}')
        await asyncio.sleep(3)
