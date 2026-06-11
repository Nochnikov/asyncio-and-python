import asyncio

import aiohttp

from learn.chapter_4.aiohttp_web_requests import fetch_status
from learn.util.async_timer import async_timed

"""
Coroutines are not canceled
When we used wait_for, if our coroutine timed out it would automatically request
cancellation for us. This is not the case with wait; it behaves closer to what we saw
with gather and as_completed. In the case we want to cancel coroutines due to a
timeout, we must explicitly loop over the tasks and cancel them.

Timeout errors are not raised
wait does not rely on exceptions in the event of timeouts as do wait_for and as_
completed. Instead, if the timeout occurs the wait returns all tasks done and all
tasks that are still pending up to that point when the timeout occurred.
"""
@async_timed()
async def main():
    # bad case. Coroutines are not canceled and still be running in the background

    # async with aiohttp.ClientSession() as session:
    #     url = 'http://example.com'
    #
    #     fetches = [
    #         asyncio.create_task(fetch_status(session, url)),
    #         asyncio.create_task(fetch_status(session, url)),
    #         asyncio.create_task(fetch_status(session, url, delay=3)),
    #     ]
    #
    #     done, pending = await asyncio.wait(fetches, timeout=0.1)
    #
    #     print('====================')
    #     print(f'DONE TASK COUNT: {len(done)}')
    #     print(f'PENDING TASK COUNT: {len(pending)}')
    #     # bad case. Coroutines are not canceled and still be running in the background
    #     for done_task in done:
    #         print(await done_task)
    """Note that, as before, our tasks in the pending set are not canceled and will continue to
    run despite the timeout. If we have a use case where we want to terminate the pending
    tasks, we’ll need to explicitly loop through the pending set and call cancel on each task."""
    async with aiohttp.ClientSession() as session:
        url = 'http://example.com'

        pending = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url, delay=3)),
        ]

        while pending:

            done, pending = await asyncio.wait(pending, timeout=1)
            print('====================')
            print(f'DONE TASK COUNT: {len(done)}')
            print(f'PENDING TASK COUNT: {len(pending)}')

            for done_task in done:
                try:
                    print(await done_task)
                except asyncio.exceptions.CancelledError:
                    pass

            for pending_task in pending:
                if not pending_task.cancelled():
                    pending_task.cancel()

asyncio.run(main())
