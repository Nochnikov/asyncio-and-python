import asyncio
from asyncio import AbstractEventLoop

from chapter_8.transport_and_protocols import HTTPGetClientProtocol


async def make_request(host: str, port: int, loop: AbstractEventLoop):
    def protocol_factory():
        return HTTPGetClientProtocol(host, loop)

    _, protocol = await loop.create_connection(protocol_factory, host, port)

    return await protocol.get_response()

async def main():
    loop = asyncio.get_running_loop()
    result = await make_request('www.example.com', 80, loop)
    print(result)

asyncio.run(main())
