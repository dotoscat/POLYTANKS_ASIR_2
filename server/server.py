# Copyright (C) 2018  Oscar 'dotoscat' Triano <dotoscat (at) gmail (dot) com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.import asyncio

import weakref
import socket
import asyncio
from polytanks import protocol, snapshot
from polytanks.event import event_manager
from .player import Player
from .engine import Engine
from .protocol import ServerProtocol

class GameProtocol(asyncio.DatagramProtocol):
    def __init__(self, server):
        self.server = server
        self.transport = None

    def datagram_received(self, data, addr):
        command = protocol.command(data)
        # print("{} bytes received from {}".format(len(data), addr))
        if command == protocol.SNAPSHOT_ACK:
            command, id = protocol.snapshotack_struct.unpack(data)
            self.server.ack_client(id)
        elif command == protocol.INPUT:
            command, id = protocol.command_id_struct.unpack_from(data)
            self.server.apply_input(id, data)

    def connection_made(self, transport):
        print("GameProtocol connection_made")
        self.transport = transport

class Server:
    SNAPSHOT_RATE = 1./15.
    def __init__(self, max_n_players, host):
        self.engine = Engine(max_n_players, max_n_players + 1)
        self.engine.load_level()
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
        GAME_RATE = 1./60.
        while True:
            # print(self, len(self.connecting_clients), self.connecting_clients.get(1))
            start = self.loop.time()
            self.clean_clients()
            self.engine.update(GAME_RATE)
            self.send_snapshot()
            self.send_events()
            total = self.loop.time() - start
            # print("took ms:", total)
            await asyncio.sleep(GAME_RATE)

    def send_events(self):
        data = event_manager.to_network()
        if not data:
            return
        data = int.to_bytes(protocol.EVENT, 1, "big") + data
        for id in self.clients:
            player = self.clients[id]
            player.secure_send(data)

    def clean_clients(self):
        offline = [id for id in self.clients
            if self.clients[id].response_time > 3.]
        for id in offline:
            self.remove_client(id)
            print("Remove client with id {}".format(id))

    def send_snapshot(self):
        if not self.clients:
            return

        current_time = self.loop.time()
        if current_time - self.last_snapshot_time < self.SNAPSHOT_RATE:
            return
        # print("send snapshot at", current_time)
        shot = snapshot.Snapshot()
        shot.from_engine(self.engine)
        for client in self.clients:
            player = self.clients[client]
            if player.game_address is None:
                continue
            player.add_snapshot(shot)
            diff_data = player.get_diff_data()
            # print("diff data", diff_data)
            data = int.to_bytes(protocol.SNAPSHOT, 1, "big")
            data += diff_data
            player.send_time = self.loop.time()
            self.game_transport.sendto(data, player.game_address)

    def apply_input(self, id, data):
        player = self.engine.entities.get(id)
        if not player:
            return
        player.input.from_bytes(data[protocol.command_id_struct.size:])

    def set_game_address(self, player_id, port):
        player = self.clients[player_id] 
        player.set_game_address(port)
        current_time = self.loop.time()
        player.ack_time = current_time
        player.send_time = current_time

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
        eng_player = self.engine.add_player(id)[1]
        eng_player.id = id
        eng_player.body.y = 128.
        eng_player.body.x = 64.
        eng_player.body.has_gravity = True
        return id

    def remove_client(self, id_):
        if not id_ in self.clients:
            return None
        player = self.clients[id_]
        self.engine.remove_player(id_)
        del self.clients[id_]
        return player

    def ack_client(self, id):
        player = self.clients.get(id)
        if not player:
            return
        player.ack(self.loop.time())

    def send_requested_snapshot(self, id):
        shot = snapshot.Snapshot()
        shot.from_engine(self.engine)
        diff_data = shot.diff(snapshot.MASTER_SNAPSHOT)
        data = int.to_bytes(protocol.SNAPSHOT, 1, "big")
        data += diff_data
        player = self.clients[id]
        player.server_transport.write(data)
        shot.free()
