import asyncio
import time
from asyncio import AbstractEventLoop
from concurrent.futures.process import ProcessPoolExecutor
from functools import partial


def count(count_to: int) -> int:
    counter = 0
    start = time.time()
    while counter < count_to:
        counter += 1
    end = time.time()

    print(f'Took {end - start}sec')
    return counter

async def main():
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_event_loop()
        nums = [3, 5, 22, 1, 100000000]

        calls: list[partial[int]] = [partial(count, num) for num in nums]
        call_cors =[]

        for call in calls:
            call_cors.append(loop.run_in_executor(process_pool, call))

        results = await asyncio.gather(*call_cors)

    for result in results:
        print(result)

if __name__ == '__main__':
    asyncio.run(main())

