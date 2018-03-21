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

import logging
import asyncio
from polytanks import protocol

class ServerProtocol(asyncio.Protocol):
    def __init__(self, server):
        self.server = server
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("Connection made", transport.get_extra_info("peername"))

    def data_received(self, data):
        # print("data_received", data, "from", self.transport.get_extra_info("peername"))
        command = protocol.command(data)
        if command == protocol.CONNECT:
            player_id = self.server.add_client(self.transport)
            if player_id:
                print("yes", player_id)
                self.transport.write(
                    protocol.connected_struct.pack(
                        protocol.CONNECTED, player_id, self.server.max_n_players))
            else:
                self.transport.write(b"NO")
        elif command == protocol.DISCONNECT:
            id_ = int.from_bytes(data[1:2], "big")
            player = self.server.clients.get(id_)
            if player:
                self.transport.write(b"OK")
                self.transport.write_eof()
                self.server.remove_client(id_)
            else:
                self.transport.write(b"NO")
        elif command == protocol.SEND_GAME_PORT:
            command, player_id, port, rudp_port = protocol.sendgameport_struct.unpack(data) 
            print("game - rudp port", player_id, port, rudp_port)
            self.server.set_game_address(player_id, port, rudp_port)
        elif command == protocol.REQUEST_SNAPSHOT:
            command, player_id = protocol.request_snapshot_struct.unpack(data)
            self.server.send_requested_snapshot(player_id)
            # print("player {} requests a full snapshot".format(player_id))
        # print("clients", self.server.clients)

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
        # print("{} bytes received from {}".format(len(data), addr))
        if command == protocol.SNAPSHOT_ACK:
            command, id = protocol.snapshotack_struct.unpack(data)
            self.server.ack_client(id)
        elif command == protocol.INPUT:
            command, id = protocol.command_id_struct.unpack_from(data)
            self.server.apply_input(id, data)

    def connection_made(self, transport):
        logging.info("GameProtocol connection_made")
        self.transport = transport