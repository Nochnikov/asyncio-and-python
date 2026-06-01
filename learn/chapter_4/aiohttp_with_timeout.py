import asyncio
import aiohttp
from aiohttp import ClientSession

async def fetch_status(
    session: ClientSession,
    url: str,
) -> int:
    # Total time for whole operation is 1 sec, connection takes 100 ms
    # if request will take more than 10 ms it will raise an exception.
    # asyncio.TimeoutError
    ten_milis = aiohttp.ClientTimeout(total=.01)
    async with session.get(url, timeout=ten_milis) as response:
        return response.status


async def main():
    # total time 1 sec, if connection will take more than 100 mili secs it
    # will raise an Exception.
    ## asyncio.TimeoutError
    session_timeout = aiohttp.ClientTimeout(total=1, connect=.1)

    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        await fetch_status(session, 'http://example.com')

asyncio.run(main())
