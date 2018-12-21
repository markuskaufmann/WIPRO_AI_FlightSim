from ch.hslu.wipro.fg.connect.tcp_socket_client import TCPSocketClient
from ch.hslu.wipro.fg.io.fg_client_write import FGClientWrite


class TCPSocketClientWrite(TCPSocketClient):

    def threaded_method(self):
        FGClientWrite.create_instance()
