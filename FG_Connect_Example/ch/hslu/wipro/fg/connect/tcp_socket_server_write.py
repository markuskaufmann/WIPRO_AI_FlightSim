from ch.hslu.wipro.fg.io.fg_client_write import FGClientWrite
from ch.hslu.wipro.fg.connect.tcp_socket_server import TCPSocketServer


class TCPSocketServerWrite(TCPSocketServer):

    def threaded_method(self, client_socket, client_address):
        print("accept write: {0}, {1}".format(client_socket, client_address))
        fg_client_write = FGClientWrite(client_socket, client_address)
        fg_client_write.start_process()
