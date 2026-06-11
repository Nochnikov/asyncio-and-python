"""
Both ALL_COMPLETED and FIRST_EXCEPTION have the drawback that, in the case where
coroutines are successful and don’t throw an exception, we must wait for all coroutines to complete.
We may use ```as_completed```, but it also has drawbacks as:
we can not see the order, which task currently running, and which task have completed.
We get them only one at a time through an iterator.

The good news is that the return_when parameter accepts a FIRST_COMPLETED
option. This option will make the wait coroutine return as soon as it has at least one
result. This can either be a coroutine that failed or one that ran successfully. We can
then either cancel the other running coroutines or adjust which ones to keep running, depending on our use case.
"""
import asyncio

import aiohttp

from learn.chapter_4.aiohttp_web_requests import fetch_status
from learn.util.async_timer import async_timed

"""Here the pending tasks will not be processed when a first task completes.
After the first task is completed the asyncio.wait(return_when=asyncio.FIRST_COMPLETED) returns control to the main 
so it will shut down. When the main coroutine are finished the event loop will 
cancel others
"""
#
# @async_timed()
# async def main():
#     async with aiohttp.ClientSession() as session:
#         url = 'http://example.com'
#
#         fetchers = [
#             asyncio.create_task(fetch_status(session, url)),
#             asyncio.create_task(fetch_status(session, url,delay=10)),
#             asyncio.create_task(fetch_status(session, url,)),
#         ]
#
#         done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_COMPLETED)
#
#         print(f'DONE TASKS COUNT {len(done)}')
#         print(f'PENDING TASKS COUNT {len(pending)}')
#
#         for done_task in done:
#             print(await done_task)
#
# asyncio.run(main())

'''
Here because of the loop all the pending tasks will be completed. 
'''
@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'http://example.com'

        pending = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url,delay=10)),
            asyncio.create_task(fetch_status(session, url,)),
        ]
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            print(f'DONE TASKS COUNT {len(done)}')
            print(f'PENDING TASKS COUNT {len(pending)}')

            for done_task in done:
                print(await done_task)

asyncio.run(main())