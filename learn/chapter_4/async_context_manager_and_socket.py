import asyncio
import socket
from types import TracebackType
from typing import Optional, Type


class ConnectionSocket:

    def __init__(self, server_socket):
        self._connection = None
        self._server_socket = server_socket

    async def __aenter__(self):
        """
        This coroutine is called when
        we enter the with block. It
        waits until a client connects
        and returns the connection.
        """
        print('Entering context manager, waiting for connection...')
        loop = asyncio.get_event_loop()
        connection, address = await loop.sock_accept(self._server_socket)
        self._connection = connection
        print('Accepted connection from {}'.format(address))
        return self._connection

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        """
        This coroutine is called when
        we exit the with block. In it,
        we clean up any resources
        we use. In this case, we close
        the connection.
        """
        print('Exiting context manager, waiting for connection...')
        self._connection.close()
        print('Closing connection...')


async def main():
    loop = asyncio.get_event_loop()

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('localhost', 8080)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    async with ConnectionSocket(server_socket) as connection:
        """
        This calls __aenter__
        and waits for a client
        connection
        """
        data = await loop.sock_recv(connection, 1024)
        """
        After this statement,
        __aenter__ will execute, and
        we’ll close our connection.
        """
        print(data)

asyncio.run(main())
