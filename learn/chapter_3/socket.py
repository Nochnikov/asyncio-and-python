import socket

"""
socket.AF_INET - this tells us what type of address our socket 
will be able to interact with:  

In this case, socket.AF_INET - a hostname and a port number

socket.SOCK_STREAM - this means that we use the TCP protocol

We also call setsockopt to set the SO_REUSEADDR flag to 1. This will allow us to reuse
the port number after we stop and restart the application, avoiding any address already
in use errors. If we didn’t do this, it might take some time for the operating system to
unbind this port and have our application start without error.
"""

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()

connection, client_address = server_socket.accept()
print(f'I got a connection from {client_address}')


