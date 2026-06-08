import asyncio

import aiohttp

from learn.chapter_4.aiohttp_web_requests import fetch_status
from learn.util.async_timer import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, 'http://example.com', 1),
            fetch_status(session, 'http://example.com', 1),
            fetch_status(session, 'http://example.com', 10),
        ]

        for finished_task in asyncio.as_completed(fetchers):
            print(await finished_task)

asyncio.run(main())