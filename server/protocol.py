# Copyright (C) 2017  Oscar 'dotoscat' Triano <dotoscat (at) gmail (dot) com>

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
            self.server.set_game_address(player_id, port)
            print("game port", player_id, port)
        elif command == protocol.REQUEST_SNAPSHOT:
            command, player_id = protocol.request_snapshot_struct.unpack(data)
            print("player {} requests a full snapshot".format(player_id))
        print("clients", self.server.clients)

    def connection_lost(self, exc):
        if not exc:
            print("Connection closed normally")
        else:
            print("error", exc)
