import asyncio

from util.input_reader import create_stdin_reader
from util.utils import delay


async def main():
    stdin_reader = await create_stdin_reader()

    while True:
        delay_time = await stdin_reader.readline()
        asyncio.create_task(delay(int(delay_time)))

asyncio.run(main())