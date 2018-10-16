import socket
from threading import Thread


class TCPSocketServer:
    HOST = "127.0.0.1"

    def __init__(self, port, backlog=1):
        self.port = port
        self.backlog = backlog
        self.closed = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.t_listen = Thread(target=self.listen)

    def start(self):
        self.t_listen.start()

    def listen(self):
        try:
            self.socket.bind((TCPSocketServer.HOST, self.port))
            self.socket.listen(self.backlog)
            print("socket server listening on: {0}:{1}".format(TCPSocketServer.HOST, self.port))
            while not self.closed:
                (client_socket, address) = self.socket.accept()
                self.threaded_method(client_socket, address)
            self.socket.close()
        except Exception as e:
            print(e)

    def threaded_method(self, client_socket, client_address):
        raise NotImplementedError("Abstract method - to be implemented in subclasses")

    def close(self):
        self.closed = True

    def is_closed(self):
        return self.closed
