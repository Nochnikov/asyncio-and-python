import asyncio

import aiohttp
from aiohttp import ClientSession

from learn.util.async_timer import async_timed


@async_timed()
async def fetch_status(
    session: ClientSession,
    url: str,
):
    async with session.get(url) as result:
        return result.status

"""Version without returning exception
Problems: 
1. Will throw exception while being operated 
2. Another potential issue with the code is that if more than one exception
happens, we’ll only see the first one that occurred when we await the gather.
"""
# @async_timed()
# async def main():
#     async with aiohttp.ClientSession() as session:
#         urls = ['http://example.com', 'python://example123.com']
#         tasks = [fetch_status(session, url) for url in urls]
#         status_code = await asyncio.gather(*tasks,)
#         print(status_code)

""" Version with returning exception
Problems: 
1. Not easy to cancel tasks. If we are requesting to the same server 
and one request failed, than other will too. We may want to cancel requests
to free up resources, which would not be easy because out 
corutines are wrapped in tasks in the background. 
2. The must wait to all tasks to be finished. We cannot manage them 
as the completed. 
"""
@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['http://example.com', 'python://example.com']

        tasks = [fetch_status(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        exceptions = [res for res in results if isinstance(res, Exception)]
        successful_results = [res for res in results if not isinstance(res, Exception)]

        print(f'All results: {results}')
        print(f'Successful results: {successful_results}')
        print(f'Finished with exceptions: {exceptions}')

asyncio.run(main())
