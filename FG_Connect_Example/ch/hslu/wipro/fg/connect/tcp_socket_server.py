import socket
from threading import Thread

from ch.hslu.wipro.fg.properties.fg_property_type import FGPropertyType


class TCPSocketServer:
    HOST = "127.0.0.1"

    def __init__(self, fg_property_type: FGPropertyType, backlog=1):
        self.fg_property_type = fg_property_type
        self.port = FGPropertyType.TYPE_CONNECTION_MAP[self.fg_property_type][0]
        self.backlog = backlog
        self.closed = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        self.t_listen = Thread(target=self.listen)

    def start(self):
        self.t_listen.start()

    def listen(self):
        try:
            self.socket.bind((TCPSocketServer.HOST, self.port))
            self.socket.listen(self.backlog)
            print("socket server listening on: {0}:{1} ({2})".format(TCPSocketServer.HOST, self.port,
                                                                     self.fg_property_type))
            FGPropertyType.add_socket_to_connection_map(self.fg_property_type, self.socket)
            while not self.closed:
                (client_socket, address) = self.socket.accept()
                self.client_socket = client_socket
                self.threaded_method(client_socket, address)
            self.socket.close()
        except Exception as e:
            print(e)

    def threaded_method(self, client_socket, client_address):
        raise NotImplementedError("Abstract method - to be implemented in subclasses")

    def close(self):
        self.closed = True

    def close_client(self):
        if self.client_socket is None:
            return
        try:
            self.client_socket.close()
        except Exception as e:
            print("Error while trying to close client socket: {0}".format(e))

    def is_closed(self):
        return self.closed
