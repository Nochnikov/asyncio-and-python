import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial

import requests

from util.async_timer import async_timed


def get_status_code(url):
    response = requests.get(url)
    return response.status_code


@async_timed()
async def main():
    loop = asyncio.get_event_loop()

    with ThreadPoolExecutor() as executor:
        urls = ['https://www.baidu.com' for _ in range(1000)]
        tasks = [loop.run_in_executor(executor, partial(get_status_code, url)) for url in urls]
        results = await asyncio.gather(*tasks)
        print(results)

asyncio.run(main())