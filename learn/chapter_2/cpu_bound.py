import asyncio

from learn.util.async_timer import async_timed

@async_timed()
async def cpu_bound_work() -> int:
    count = 0

    for i in range(100000000):
        count += 1
    return count

@async_timed()
async def main():
    task_one = asyncio.create_task(cpu_bound_work())
    # task_two = asyncio.create_task(cpu_bound_work())

    await task_one
    # await task_two


asyncio.run(main(), debug=True)
