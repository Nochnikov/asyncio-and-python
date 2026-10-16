import socket
from threading import Thread


def echo(client: socket):
    while True:
        data = client.recv(2048)
        print(f'Received {data}, sending!')
        client.send(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 8000))
    s.listen()
    while True:
        # blocking request to client connect
        connection, _ = s.accept()
        # when connection accepted create new thread to run function
        thread = Thread(target=echo, args=(connection,))
        # starting the thread
        thread.start()