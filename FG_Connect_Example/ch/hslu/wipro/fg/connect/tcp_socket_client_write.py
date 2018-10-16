from ch.hslu.wipro.fg.connect.tcp_socket_client import TCPSocketClient
from ch.hslu.wipro.fg.io.fg_client_write import FGClientWrite


class TCPSocketClientWrite(TCPSocketClient):

    def threaded_method(self):
        fg_client_write = FGClientWrite(self.socket, None)
        fg_client_write.start_process()
