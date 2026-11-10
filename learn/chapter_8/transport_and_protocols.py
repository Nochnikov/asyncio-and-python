import asyncio
from asyncio import AbstractEventLoop, Future, Transport
from typing import Optional


class HTTPGetClientProtocol(asyncio.Protocol):

    def __init__(self, host: str, loop: AbstractEventLoop):
        self._host = host
        self._future: Future = loop.create_future()
        self._transport: Optional[Transport] = None
        self._response_buffer: bytes = b''

    async def get_response(self):
        # Await the whole future unless we got a response for the server
        return await self._future

    def _get_request_bytes(self) -> bytes:
        # Create the HTTP request
        request = (f"GET / HTTP/1.1\r\n"
                   f"Connection: close\r\n"
                   f"Host: {self._host}\r\n\r\n")
        return request.encode()

    def connection_made(self, transport: Transport):
        print(f'Connection made to {self._host}')
        self._transport = transport
        # Once we've established a connection, use the transport to send the request
        self._transport.write(self._get_request_bytes())

    def data_received(self, data):
        print(f'Data received from {self._host}')
        # Once we have data, save it to our internal buffer
        self._response_buffer += data

    def eof_received(self) -> Optional[bool]:
        # Once the connection closes, complete the future with the buffer
        self._future.set_result(self._response_buffer.decode())
        return False

    def connection_lost(self, exc: Optional[Exception]) -> None:
        # if the connection closes without error, do nothing; otherwise,
        # complete the future with an exception
        if exc is None:
            print(f'Connection lost to {self._host}')
        else:
            self._future.set_exception(exc)
