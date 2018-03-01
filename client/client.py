import socket
import selectors
from polytanks import protocol

class Client:
    def __init__(self):
        self.selectors = selectors.DefaultSelector()
        self.server_address = None
        self.id = 0
        self.server_connection = None
        self.game_connection = None
        self.server_callback = None
        self.control_register = None
        self.success_callback = None

    def __del__(self):
        self.selectors.close()

    @property
    def connected(self):
        return self.id > 0
    
    def step(self):
        if not self.control_register:
            return
        events = self.selectors.select(0)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj)

    def game_send(self, data):
        self.game_connection.sendall(data)

    def server_send(self, data):
        self.server_connection.sendall(data)

    def manage_server_connection(self, socket):
        data = socket.recv(1024)
        command = protocol.command(data)
        if data == b'OK':
            self._disconnected()
        elif command == protocol.CONNECTED:
            self._connected(data)
        else:
            self.server_callback(data)
    
    def _connected(self, response):
        print("connected", response)
        self.id = int.from_bytes(response[1:2], "big")
        self.game_connection = socket.socket(type=socket.SOCK_DGRAM)
        print("server_address", self.server_address)
        self.game_connection.setblocking(False)
        self.game_connection.connect(self.server_address)
        game_address = self.game_connection.getsockname()
        print("game_connection port", game_address)
        self.server_connection.send(
            protocol.sendgameport_struct.pack(protocol.SEND_GAME_PORT, self.id, game_address[1]))
        self.selectors.register(self.game_connection, selectors.EVENT_READ, self.game_callback)
        self.success_callback()
        self.success_callback = None
    
    def _disconnected(self):
        self.success_callback()
        self.success_callback = None
        self.id = 0
        self.control_register = None
        self.server_address = None
        self.selectors.unregister(self.game_connection)
        self.selectors.unregister(self.server_connection)
        self.game_connection.close()
        self.server_connection.close()

    def connect_to_server(self, address, callback, server_callback, success_callback):
        if not callable(callback):
            raise TypeError("callback is not callable. Passed {} instead.".format(type(callback)))
        if not callable(success_callback):
            raise TypeError("success_callback is not callable. Passed {} instead.".format(type(success_callback)))
        if self.connected:
            return
        self.server_connection = socket.socket()
        self.server_connection.connect(address)
        self.server_connection.setblocking(False)
        self.server_connection.send(protocol.CONNECT.to_bytes(1, "big"))
        self.control_register = self.selectors.register(self.server_connection,
            selectors.EVENT_READ, self.manage_server_connection)
        # print(self.server_connection.recv(1024))
        self.server_address = address
        self.game_callback = callback
        self.server_callback = server_callback
        self.success_callback = success_callback
        # self.server_connection.close()

    def disconnect_from_server(self, success_callback):
        if not callable(success_callback):
            raise TypeError("success_callback is not callable. {} passed".format(success_callback))
        if not self.connected:
            return
        self.success_callback = success_callback
        self.server_connection.send(
            protocol.disconnect_struct.pack(protocol.DISCONNECT, self.id))
