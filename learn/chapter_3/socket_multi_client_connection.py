import socket
"""
This code is able to handle multiple connections from clients. 
However there are still two main problems: 
   1. Sockets are blocking by default. 
       It means that while first client connected and 
       does not send their first message 
       second one will be blocked and will not receive anything
       This causes other clients to be stuck waiting for the next iteration of the loop, 
       which won’t happen until the first client sends us data. Picture 1 in chapter_3/README.MD 
   2. Non-blocking sockets requires connections immediately.
      Like if we run that application mostly we would have an error like 
      ``BlockingIOError``` which means that socker has no connection yet 
      and therefor no data to process.
      So, the easiest solution is to catch that error, ignore it, and keep 
      looping until we have data.
      With this tactic, we’ll constantly be checking for new connections and data
      as fast as we can. This should solve the issue that our blocking socket echo server had.

However by this code client now not depend on one another, this is not 
an effective solution yet. Catching any time when exception pops up may lead 
to potentially error-prone, also it takes a lot of resource. 
The second is a resource issue. This application will always
be using nearly 100% of our CPU’s processing power. This is because we
are constantly looping and getting exceptions as fast as we can inside our application,
leading to a workload that is CPU heavy. Picture 2 in chapter_3/README.MD
"""

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(('localhost', 8000))
server_socket.listen()
# set non-blocking mode to resolve first problem.
"""
Fundamentally, creating a non-blocking socket is no different from creating a blocking one, 
except that we must call setblocking with False
"""
server_socket.setblocking(False)

connections = []
try:
    while True:
        try:
            connection, client_address = server_socket.accept()
            # mark client socket as non-blocking
            connection.setblocking(False)
            print(f'I got a connection from {client_address}!')
            connections.append(connection)
        except BlockingIOError:
            pass

        for connection in connections:
            try:
                buffer = b''

                while buffer[-2:] != b'\r\n':
                    data = connection.recv(2)

                    if not data:
                        break
                    else:
                        print(f'I got data: {data}!')
                        buffer += data
                print(f'All the data is: {buffer}')

                buffer = buffer.replace(b'\r\n', b'')
                buffer += b' send_back\r\n'

                connection.send(buffer)
            except BlockingIOError:
                pass
finally:
    server_socket.close()