import asyncio
from unittest import result

import aiohttp

from learn.chapter_4.aiohttp_web_requests import fetch_status
from learn.util.async_timer import async_timed

"""
Even though that this code completes faster due to timeout 
also it does not throw and exception there are still two problem: 
1. there isn’t any way to easily see which
coroutine or task we’re awaiting as the order is completely nondeterministic. If we
don’t care about order, this may be fine, but if we need to associate the results to the
requests somehow, we’re left with a challenge

2. while we will correctly throw an exception and
move on, any tasks created will still be running in the background. Since it’s hard to
figure out which tasks are still running if we want to cancel them, we have another
challenge.
"""
@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, 'http://example.com', 1),
            fetch_status(session, 'http://example.com', 10),
            fetch_status(session, 'http://example.com', 10),
        ]

        for done_task in asyncio.as_completed(fetchers, timeout=2):
            try:
                result = await done_task
                print(result)
            except asyncio.TimeoutError:
                print('Timeout error')


        for task in asyncio.tasks.all_tasks():
            print(task)

asyncio.run(main())
