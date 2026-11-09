import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Lock

import requests

from util.async_timer import async_timed

counter_lock = Lock()
counter: int = 0

def get_status_code(url: str):
    global counter
    response = requests.get(url)

    with counter_lock:
        counter += 1

    return response.status_code


async def reporter(request_count: int):
    while counter < request_count:
        print(f'Finished {counter}/{request_count} requests')
        await asyncio.sleep(0.5)

@async_timed()
async def main():
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor() as executor:
        request_count = 200
        urls = ['https://www.example.com' for _ in range(request_count)]
        reporter_task = asyncio.create_task(reporter(request_count))

        tasks = [loop.run_in_executor(executor, get_status_code, url) for url in urls]

        results = await asyncio.gather(*tasks)

        await reporter_task
        print(results)

asyncio.run(main())
