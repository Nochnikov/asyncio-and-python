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


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'http://www.example.com'
        status = await fetch_status(session, url)
        print(f'Status for {url} was {status}')

asyncio.run(main())