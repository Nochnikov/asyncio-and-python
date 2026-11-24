import asyncio
import logging
from asyncio import StreamWriter, StreamReader


class ServerState:
    def __init__(self) -> None:
        self._writers = []

    async def add_client(self, reader: StreamReader, writer: StreamWriter) -> None:
        self._writers.append(writer)
        await self._on_connect(writer)
        asyncio.create_task(self._echo(reader, writer))

    async def _on_connect(self, writer: StreamWriter):
        # On a new connection tell the client how many users are online,
        # and notify others of a new user
        writer.write(f'Welcome! {len(self._writers)} user (s) are online!\n'.encode())
        await writer.drain()
        await self._notify_all('New user connected!\n')

    # Handle echoing user input when a client disconnects,
    # and notify other users of a disconnect
    async def _echo(self, reader: StreamReader, writer: StreamWriter) -> None:
        try:
            while (data := await reader.readline()) != b'':
                writer.write(data)
                await writer.drain()
            self._writers.remove(writer)
            await self._notify_all(f'Client disconnected. {len(self._writers)} user(s) are online!\n')
        except Exception as e:
            logging.exception('Error reading from client.', exc_info=e)
            self._writers.remove(writer)

    # helper method to send a message to all other users.
    # If a message fails to send, remove that user.
    async def _notify_all(self, msg: str) -> None:
        for writer in self._writers:
            try:
                writer.write(msg.encode())
                await writer.drain()
            except ConnectionError as e:
                logging.exception('Could not write to client.', exc_info=e)
                self._writers.remove(writer)

async def main():
    server_state = ServerState()

    async def client_connected(reader: StreamReader, writer: StreamWriter) -> None:
        # When a client connects, add that client to the server state
        await server_state.add_client(reader, writer)

    # Start the server and start serving forever. 
    server = await asyncio.start_server(client_connected, '127.0.0.1', 8000)

    async with server:
        await server.serve_forever()

asyncio.run(main())