from ch.hslu.wipro.fg.io.fg_client_read import FGClientRead
from ch.hslu.wipro.fg.connect.tcp_socket_server import TCPSocketServer


class TCPSocketServerRead(TCPSocketServer):

    def threaded_method(self, client_socket, client_address):
        print("accept read: {0}, {1}".format(client_socket, client_address))
        fg_client_read = FGClientRead(client_socket, client_address)
        fg_client_read.start_process()
