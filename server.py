#/usr/bin/env python
import sys
import weakref
import socket
import asyncio
import signal
from polytanks import protocol
signal.signal(signal.SIGINT, signal.SIG_DFL)

HOST = ("127.0.0.1", 1337)

class Player:
    def __init__(self, transport):
        self.server_transport = transport
        self.game_port = None
        self.send_time = 0.
        self.ack_time = 0.
    @property
    def offline_by(self, time, current_time):
        return self.ack_time < current_time and current_time - self.send_time > time 
    def __del__(self):
        print("close transport")
        self.server_transport.close()
    def set_game_address(self, port):
        """
        Parameters:
            port (int): Port of the udp connection
        """
        client_address = self.server_transport.get_extra_info("peername")
        self.game_address = (client_address[0], port)
    @property
    def ping(self):
        return (self.ack_time - self.send_time)/2.

class ServerProtocol(asyncio.Protocol):
    def __init__(self, server):
        self.server = server
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("Connection made", transport.get_extra_info("peername"))

    def data_received(self, data):
        print("data_received", data, "from", self.transport.get_extra_info("peername"))
        command = protocol.command(data)
        if command == protocol.CONNECT:
            player_id = self.server.add_client(self.transport)
            if player_id:
                self.transport.write(
                    protocol.connected_struct.pack(protocol.CONNECTED, player_id))
            else:
                self.transport.write(b"NO")
        elif command == protocol.DISCONNECT:
            id_ = int.from_bytes(data[1:2], "big")
            player = self.server.remove_client(id_)
            if player:
                self.transport.write(b"OK")
            else:
                self.transport.write(b"NO")
        elif command == protocol.SEND_GAME_PORT:
            command, player_id, port = protocol.sendgameport_struct.unpack(data) 
            self.server.clients[player_id].set_game_address(port)
            print("game port", player_id, port)
        print("clients", self.server.clients)

    def connection_lost(self, exc):
        if not exc:
            print("Connection closed normally")
        else:
            print("error", exc)

class GameProtocol(asyncio.DatagramProtocol):
    def __init__(self, server):
        self.server = server
        self.transport = None

    def datagram_received(self, data, addr):
        command = protocol.command(data)
        print("{} bytes received from {}".format(len(data), addr))
        if command == protocol.SNAPSHOT_ACK:
            command, id = protocol.snapshotack_struct.unpack(data)
            self.server.ack_client(id)

    def connection_made(self, transport):
        print("GameProtocol connection_made")
        self.transport = transport

class Server:
    SNAPSHOT_RATE = 1./20.
    def __init__(self, max_n_players, host=HOST):
        self.clients = {}
        self.max_n_players = max_n_players
        self.last_snapshot_time = 0.
        self.loop = asyncio.get_event_loop()
        self.server_coro = self.loop.create_server(
            lambda: ServerProtocol(weakref.proxy(self)), *host)
        self.server = self.loop.run_until_complete(self.server_coro)
        game_socket = socket.socket(type=socket.SOCK_DGRAM)
        game_socket.setblocking(False)
        game_socket.bind(host)
        self.game_coro = self.loop.create_datagram_endpoint(
            lambda: GameProtocol(weakref.proxy(self)), sock=game_socket
        )
        self.game_transport, self.game = self.loop.run_until_complete(self.game_coro)
        self.loop.run_until_complete(self.step())

    async def step(self):
        self.last_snapshot_time = self.loop.time()
        while True:
            self.send_snapshot()
            await asyncio.sleep(1./60.)
 
    def send_snapshot(self):
        current_time = self.loop.time()
        if current_time - self.last_snapshot_time < self.SNAPSHOT_RATE:
            return
        # print("send snapshot at", current_time)
        for client in self.clients:
            player = self.clients[client]
            print("player ping", player.ping)
            data = int.to_bytes(protocol.SNAPSHOT, 1, "big")
            data += b"snapshot"
            player.send_time = self.loop.time()
            self.game_transport.sendto(data, player.game_address)

    def run(self):
        try:
            self.loop.run_forever()
        finally:
            self.server.close()
            self.loop.run_until_complete(self.server.wait_closed())
            self.loop.close()
    
    @property
    def is_full(self):
        return len(self.clients) >= self.max_n_players

    def add_client(self, transport):
        if self.is_full:
            return 0
        id = 0
        for i in range(1, self.max_n_players + 1):
            if i in self.clients:
                continue
            id = i
            break
        self.clients[id] = Player(transport)
        return id

    def remove_client(self, id_):
        if not id_ in self.clients:
            return None
        player = self.clients[id_]
        del self.clients[id_]
        return player

    def ack_client(self, id):
        self.clients[id].ack_time = self.loop.time()

if __name__ == "__main__":
    print("Hola mundo")
    server = Server(2)
    server.run()
