from ch.hslu.wipro.fg.connect.tcp_socket_client import TCPSocketClient
from ch.hslu.wipro.fg.connect.tcp_socket_client_write import TCPSocketClientWrite
from ch.hslu.wipro.fg.connect.tcp_socket_server import TCPSocketServer
from ch.hslu.wipro.fg.connect.tcp_socket_server_read import TCPSocketServerRead
from ch.hslu.wipro.fg.properties.fg_property_type import FGPropertyType


class FGInit:

    # connections
    _conn_read: TCPSocketServer = None
    _conn_write_reset: TCPSocketClient = None
    _conn_write_control: TCPSocketClient = None

    # init flags
    _init_read = False
    _init_write = False

    @staticmethod
    def init_read_connection():
        if FGInit._init_read:
            return
        print("Init read server socket")
        FGInit._conn_read = TCPSocketServerRead(FGPropertyType.READ)
        FGInit._conn_read.start()
        FGInit._init_read = True

    @staticmethod
    def init_write_connections():
        if FGInit._init_write:
            return
        print("Init write client sockets")
        FGInit._conn_write_reset = TCPSocketClientWrite(FGPropertyType.WRITE_RESET)
        FGInit._conn_write_control = TCPSocketClientWrite(FGPropertyType.WRITE_CONTROL)
        FGInit._conn_write_reset.start()
        FGInit._conn_write_control.start()
        FGInit._init_write = True

    @staticmethod
    def close_read_client_connection():
        print("Close read client socket")
        FGInit._conn_read.close_client()

    @staticmethod
    def close_write_connections():
        if not FGInit._init_write:
            return
        print("Close write client sockets")
        FGInit._conn_write_control.close()
        FGInit._conn_write_reset.close()
        FGInit._init_write = False
