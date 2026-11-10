import asyncio
from asyncio import StreamReader
from typing import AsyncGenerator


async def read_until_empty(stream_reader: StreamReader) -> AsyncGenerator[str, None]:
    # Read a line and decode it until we don't have any left
    while response := await stream_reader.readline():
        yield response.decode()

async def main():
    host: str = 'www.example.com'
    request: str = (f"GET / HTTP/1.1\r\n"
               f"Connection: close\r\n"
               f"Host: {host}\r\n\r\n")

    stream_reader, stream_writer = await asyncio.open_connection(host, 80)

    try:
        # Write the http request, and drain the writer
        stream_writer.write(request.encode())
        await stream_writer.drain()

        # read each line, and store it in a list
        responses = [response async for response in read_until_empty(stream_reader)]

        print(''.join(responses))
    finally:
        # Close the writer, and wait for it to finish closing
        stream_writer.close()
        await stream_writer.wait_closed()

asyncio.run(main())