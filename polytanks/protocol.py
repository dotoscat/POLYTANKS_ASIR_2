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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import struct

CONNECT = 1
CONNECTED = 2
SEND_GAME_PORT = 3
DISCONNECT = 4
SNAPSHOT = 5
SNAPSHOT_ACK = 6
INPUT = 7
REQUEST_SNAPSHOT = 9

# CONNECT is send as a single byte
connected_struct = struct.Struct("!BB")
disconnect_struct = struct.Struct("!BB")
snapshot_struct = struct.Struct("!BB")
snapshotack_struct = struct.Struct("!BB")
sendgameport_struct = struct.Struct("!BBH")
input_struct = struct.Struct("!BBf") # TODO: Add jump press, shoot press and cannon angle later
request_snapshot_struct = struct.Struct("!BB")

def command(data):
    return int.from_bytes(data[:1], "big")
