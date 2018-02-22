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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import deque
from polytanks.snapshot import PlayerSnapshot, MAX_SNAPSHOTS

class Player:
    MAX_SNAPSHOTS = 32
    def __init__(self, transport):
        self.server_transport = transport
        self.game_address = None
        self.send_time = 0.
        self.ack_time = 0.
        self.snapshots = deque()

    def __del__(self):
        while(self.snapshots):
            snapshot = self.snapshots.pop()
            snapshot.free()
        print("close transport")
        self.server_transport.close()

    def add_snapshot(self, snapshot):
        snapshot.borrow()
        self.snapshots.appendleft(snapshot)
        if(len(self.snapshots) >= MAX_SNAPSHOTS):
            removed = self.snapshots.pop()
            removed.free()

    def set_game_address(self, port):
        """
        Parameters:
            port (int): Port of the udp connection
        """
        client_address = self.server_transport.get_extra_info("peername")
        self.game_address = (client_address[0], port)

    @property
    def ping(self):
        return (self.send_time - self.ack_time)/2.

    @property
    def response_time(self):
        return self.send_time - self.ack_time
