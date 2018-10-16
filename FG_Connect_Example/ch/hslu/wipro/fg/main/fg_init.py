from ch.hslu.wipro.fg.connect.tcp_socket_client_write import TCPSocketClientWrite
from ch.hslu.wipro.fg.connect.tcp_socket_server_read import TCPSocketServerRead
from ch.hslu.wipro.fg.properties.fg_property_type import FGPropertyType


class FGInit:

    # connections
    conn_read = None
    conn_write_reset = None
    conn_write_control = None
    conn_write_engine = None
    conn_write_gear = None

    def init_read_connection(self):
        self.conn_read = TCPSocketServerRead(FGPropertyType.TYPE_PORT_MAP[FGPropertyType.READ])
        self.conn_read.start()

    def init_write_connections(self):
        self.conn_write_reset = TCPSocketClientWrite(FGPropertyType.TYPE_PORT_MAP[FGPropertyType.WRITE_RESET])
        self.conn_write_control = TCPSocketClientWrite(FGPropertyType.TYPE_PORT_MAP[FGPropertyType.WRITE_CONTROL])
        self.conn_write_engine = TCPSocketClientWrite(FGPropertyType.TYPE_PORT_MAP[FGPropertyType.WRITE_ENGINE])
        self.conn_write_gear = TCPSocketClientWrite(FGPropertyType.TYPE_PORT_MAP[FGPropertyType.WRITE_GEAR])
        self.conn_write_reset.start()
        self.conn_write_control.start()
        self.conn_write_engine.start()
        self.conn_write_gear.start()
