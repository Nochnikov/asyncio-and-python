import socket
from ssl import socket_error
from threading import Thread


class ClientEchoThread(Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        try:
            while True:
                data = self.client.recv(2048)
                if not data:
                    # if not data raise an exception. Usually happens when connection closed by
                    # user or was shut down
                    raise BrokenPipeError('Connection closed!')
                print(f'Received {data}, sending!')
                self.client.sendall(bytes("Hello? Anyone here?\n", encoding="utf-8"))
        except OSError as e:
            # Exiting method if exception acquired. Terminates the thread.
            print(f'Thread interrupted by {e} exception, shutting down!')

    def close(self):
        # if thread is alive -> shit it down
        if self.is_alive():
            self.client.sendall(bytes("Goodbye! Thank you for your time!\n", encoding="utf-8"))
            self.client.shutdown(socket.SHUT_RDWR) # shut down client connections for read and write


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind(('127.0.0.1', 8000))
    serv.listen()
    connection_threads = []

    try:
        while True:
            connection, addr = serv.accept()
            thread = ClientEchoThread(connection)
            connection_threads.append(thread)
            thread.start()
    except KeyboardInterrupt:
        print('Shutting down...')
        [thread.close() for thread in connection_threads]