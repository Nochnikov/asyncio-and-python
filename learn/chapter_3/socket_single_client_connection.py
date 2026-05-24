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

"""
so mostly sockets use telnet in order to have two-pointed connections

to see that have to use ```telnet **your host** **your port**```
"""
try:
    connection, client_address = server_socket.accept()
    print(f'I got a connection from {client_address}')

    buffer = b''
    """
    as we have already seen method ```.accept() returned tuple 
    with two arguments.  
    
    variable ```connection``` (which is client socket actually) is a socket object, and has 
    a method named ```recv``` that we have to use to get 
    data from a particular socket. The method takes as an integer 
    the number of bytes we want to receive from the socket. It calls 
    ```buff_size```
    
    In this case, we’ll treat the end of input as a carriage return plus a line feed or
    "/r/n" 
    
    In large application we mostly would be using numbers such as 1024, 
    'cause it will take advantage of the
    buffering that occurs at the operating system-level, 
    which is more efficient than doing it in your application.
    (1024 bytes), however for now 2 bytes per iteration is much efficient. 
    """
    while buffer[-2:] != b'\r\n':
        data = connection.recv(2)
        if not data:
            break
        else:
            print(f'I got data: {data}')
            buffer += data

    print(f'All the data is: {buffer}')
    buffer = buffer.replace(b'\r\n', b'')
    buffer += b' send_back\r\n'
    """
    To send back some message from one socket to another 
    we have method named ```.sendall()`` which takes 
    your back sent message. 
    
    In this practically example we have created 
    basic echo server with sockets. 
    
    However this application handles only one 
    client at a time right now, nevertheless 
    multiple clients are able to connect to 
    the a single server socket. 
    """
    connection.sendall(buffer)
finally:
    server_socket.close()
