"""wait in asyncio is similar to gather wait that offers more specific control to handle
these situations. This method has several options to choose from depending on when
we want our results. In addition, this method returns two sets: a set of tasks that are
finished with either a result or an exception, and a set of tasks that are still running.
This function also allows us to specify a timeout that behaves differently from how
other API methods operate; it does not throw exceptions. When needed, this function
can solve some of the issues we noted with the other asyncio API functions we’ve used
so far.

The basic signature of wait is a list of awaitable objects, followed by an optional
timeout and an optional return_when string. This string has a few predefined values
that we’ll examine: ALL_COMPLETED, FIRST_EXCEPTION and FIRST_COMPLETED. It defaults
to ALL_COMPLETED.
"""
import asyncio
import logging

import aiohttp

from learn.chapter_4.aiohttp_web_requests import fetch_status
from learn.util.async_timer import async_timed

"""If one of our requests throws an exception, it won’t be thrown at the asyncio.wait
call in the same way that asyncio.gather did. In this instance, we’ll get both the done
and pending sets as before, but we won’t see an exception until we await the task in
done that failed"""
# @async_timed()
# async def main():
#     async with aiohttp.ClientSession() as session:
#         fetchers = [
#             asyncio.create_task(fetch_status(session, 'http://example.com')),
#             asyncio.create_task(fetch_status(session, 'http://example.com')),
#         ]
#
#         done, pending = await asyncio.wait(fetchers)
#
#         print(f'Done task count: {len(done)}')
#         print(f'Pending task count: {len(pending)}')
#
#         for done_task in done:
#             result = await done_task
#             print(f'Done task res: {result}')

"""Example with bad request"""
@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'http://example.com')),
            asyncio.create_task(fetch_status(session, 'python://example2.com')),
        ]

        done, pending = await asyncio.wait(fetchers)

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            # result = await done_task this will throw and exception

            if done_task.exception() is None:
                print(f'Done task res: {done_task.result()}')
            else:
                logging.error("Request got an exception",
                              exc_info=done_task.exception())

asyncio.run(main())