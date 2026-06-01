import asyncio
import aiohttp
from aiohttp import ClientSession

from learn.chapter_4.aiohttp_web_requests import fetch_status
from learn.util.async_timer import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['http://example.com' for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]

        # Wait for all requests to complete
        # will wrap all the coroutines in the task
        # and run them concurrently
        status_code = await asyncio.gather(*requests)
        print(status_code)

asyncio.run(main())

"""
One of the main advantages of .gather is that all the stuff 
that have been passed in to the function will be retunrned in the
same order. 

Actually, .gather is using a special kind of ```future```. That special 
```furure`` will be marked when all the tasks are completed.  
"""
