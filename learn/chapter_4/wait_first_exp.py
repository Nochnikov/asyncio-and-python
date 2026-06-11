"""
Mostly ```wait``` with property ```all_completed``` is similar to ```gather```
Like, event though we may consume error after the all tasks completes we still
need to wait to all of them.

So what if we need to make sure every task will complete with no exception?
What if we need to allow tasks to process until first exception?

To support these use cases, wait supports the FIRST_EXCEPTION option. When we
use this option, we’ll get two different behaviors, depending on whether any of our
tasks throw exceptions.

BEHAVIORS:
    1. No exceptions from any awaitables
    If we have no exceptions from any of our tasks, then this option is equivalent to
    ALL_COMPLETED. We’ll wait for all tasks to finish and then the done set will contain
    all finished tasks and the pending set will be empty.

    2. One or more exception from a task
    if any task throws an exception, wait will immediately return once that exception is
    thrown. The done set will have any coroutines that finished successfully alongside
    any coroutines with exceptions. The done set is, at minimum, guaranteed to have one
    failed task in this case but may have successfully completed tasks. The pending set
    may be empty, but it may also have tasks that are still running. We can then use this
    pending set to manage the currently running tasks as we desire.
"""
import asyncio
import logging

import aiohttp

from learn.chapter_4.aiohttp_web_requests import fetch_status
from learn.util.async_timer import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'pythonn:://bad.com')),
            asyncio.create_task(fetch_status(session, 'http://example.com', delay=3)),
            asyncio.create_task(fetch_status(session, 'http://example.com', delay=3)),
        ]

        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_EXCEPTION)

        print(f'DONE TASK COUNT: {len(done)}')
        print(f'PENDING TASK COUNT: {len(pending)}')

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error(f'DONE TASK EXCEPTION: {done_task.exception()}')

        for pending_task in pending:
            pending_task.cancel()

asyncio.run(main())

"""NOTE Our application took almost no time to run, as we quickly reacted to
the fact that one of our requests threw an exception; the power of using this
option is we achieve fail fast behavior, quickly reacting to any issues that arise."""