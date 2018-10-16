import socket
from threading import Thread


class TCPSocketClient:
    HOST = "127.0.0.1"

    def __init__(self, port):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(20)
        self.t_connect = Thread(target=self.connect)

    def start(self):
        self.t_connect.start()

    def connect(self):
        self.socket.connect((TCPSocketClient.HOST, self.port))
        print("socket client connected to: {0}:{1}".format(TCPSocketClient.HOST, self.port))
        self.threaded_method()

    def threaded_method(self):
        raise NotImplementedError("Abstract method - to be implemented in subclasses")

    def close(self):
        self.socket.close()
