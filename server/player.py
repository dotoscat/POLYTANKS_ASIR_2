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

from collections import deque
from itertools import islice
from polytanks.snapshot import PlayerSnapshot, MAX_SNAPSHOTS, MASTER_SNAPSHOT

class Player:
    MAX_SNAPSHOTS = 32
    def __init__(self, transport):
        self.server_transport = transport
        self.game_address = None
        self.rudp_address = None
        self.send_time = 0.
        self.ack_time = 0.
        self.snapshots = deque()

    def __del__(self):
        while(self.snapshots):
            snapshot = self.snapshots.pop()
            snapshot.free()
        print("close transport")
        self.server_transport.close()

    def ack(self, time):
        if not self.snapshots:
            return
        self.ack_time = time
        self.snapshots[0].ack = True
        # print("ack", self.snapshots[0])

    def add_snapshot(self, snapshot):
        snapshot.borrow()
        player_snapshot = PlayerSnapshot()
        player_snapshot.snapshot = snapshot
        self.snapshots.appendleft(player_snapshot)
        if(len(self.snapshots) >= Player.MAX_SNAPSHOTS):
            removed = self.snapshots.pop()
            removed.free()

    def get_diff_data(self):
        if not self.snapshots:
            return b''
        first_snapshot = self.snapshots[0].snapshot
        #print("first snapshot ack", self.snapshots[0], self.snapshots[0].ack)
        for snapshot in islice(self.snapshots, 1, None):
            # print("this", snapshot, snapshot.ack)
            if not snapshot.ack:
                continue
            return first_snapshot.diff(snapshot.snapshot) 
        # print("do with master snapshot")
        return first_snapshot.diff(MASTER_SNAPSHOT)

    def set_game_address(self, port, rudp_port):
        """
        Parameters:
            port (int): Port of the game udp connection
            rudp_port (int): Port of the game rudp connection
        """
        client_address = self.server_transport.get_extra_info("peername")
        self.game_address = (client_address[0], port)
        self.rudp_address = (client_address[0], rudp_port)

    @property
    def ping(self):
        return (self.send_time - self.ack_time)/2.

    @property
    def response_time(self):
        return self.send_time - self.ack_time

    def secure_send(self, data):
        """
        Deprecated
        """
        import socket
        player_socket = self.server_transport.get_extra_info("socket")
        print("player delay", player_socket.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY))
        self.server_transport.write(data)
