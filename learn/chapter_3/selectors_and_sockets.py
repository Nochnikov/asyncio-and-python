"""
Operating systems have efficient APIs that let us watch sockets for incoming data
and other events built in. We give them a list of sockets we want to monitor
for events, and instead of constantly each socket to see if it has data,
the operating system tell us exactly when socket have data.

In the background, this is performed by a few different event notification systems,
depending on which operating system we’re running. asyncio is abstracted enough
that it switches between the different notification systems, depending on which one
our operating system supports. The following are the event notification systems used
by specific operating systems:
 kqueue—FreeBSD and MacOS
 epoll—Linux
 IOCP (I/O completion port)—Windows

It is implemented at the hardwarw level, and uses tiny CPU utilization
duting monitoring, allowing effecient resource usage. This is the core
of asyncio achives concurancy. picture 3 in chapter_3/README.MD
"""

import selectors
import socket
from selectors import SelectorKey

selector = selectors.DefaultSelector()

server_socker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socker.setblocking(False)
server_socker.bind(server_address)
server_socker.listen()

# Register our socket in the selector
selector.register(server_socker, selectors.EVENT_READ, )

while True:
    # Create a selector that will timeout after 1 second.
    events: list[tuple[SelectorKey, int]] = selector.select(timeout=1)

    if len(events) == 0:
        # If there are no events, print it out. This happens when a timeout occurs.
        print('No events, waiting a bit more!')

    for event, _ in events:
        # Get the socket for the event, which is stored in the fileobj field
        event_socket = event.fileobj

        if event_socket == server_socker:
            connection, client_address = server_socker.accept()
            connection.setblocking(False)

            print('Accepted connection from ', client_address)

            # Register the client that connected with our selector.
            selector.register(connection, selectors.EVENT_READ)
        else:
            # If the event socket is not the server socket, receive data from the client, and echo it back.
            data = event_socket.recv(1024)
            print(f'I got some data: {data}')
            event_socket.send(data)


