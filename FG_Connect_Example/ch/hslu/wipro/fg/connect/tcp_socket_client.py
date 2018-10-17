import socket
from threading import Thread

from ch.hslu.wipro.fg.properties.fg_property_type import FGPropertyType


class TCPSocketClient:
    HOST = "127.0.0.1"

    def __init__(self, fg_property_type: FGPropertyType):
        self.fg_property_type = fg_property_type
        self.port = FGPropertyType.TYPE_CONNECTION_MAP[self.fg_property_type][0]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(None)
        self.t_connect = Thread(target=self.connect)

    def start(self):
        self.t_connect.start()

    def connect(self):
        self.socket.connect((TCPSocketClient.HOST, self.port))
        print("socket client connected to: {0}:{1} ({2})".format(TCPSocketClient.HOST, self.port,
                                                                 self.fg_property_type))
        FGPropertyType.add_socket_to_connection_map(self.fg_property_type, self.socket)
        self.threaded_method()

    def threaded_method(self):
        raise NotImplementedError("Abstract method - to be implemented in subclasses")

    def close(self):
        self.socket.close()
