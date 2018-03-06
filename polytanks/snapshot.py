# Copyright (C) 2018  Oscar 'dotoscat' Triano    <dotoscat (at) gmail (dot) com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.#Copyright (C) 2017  Oscar 'dotoscat' Triano <dotoscat (at) gmail (dot) com>

import struct
import toyblock3

MAX_SNAPSHOTS = 64*4

class Body_:
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.vel_x = 0.
        self.vel_y = 0.

    def reset(self):
        self.x = 0.
        self.y = 0.
        self.vel_x = 0.
        self.vel_y = 0.

    def diff(self, body):
        return (self.x != body.x or self.y != body.y
        or self.vel_x != body.vel_x or self.vel_y != body.vel_y)

Body = toyblock3.Pool(Body_, MAX_SNAPSHOTS*4)

body_struct = struct.Struct("!Bffff") # TODO: send velocity

class MASTER_SNAPSHOT:
    players = {}

class SnapshotMixin:
    def __init__(self):
        self.players = {}
        self._borrowed = 0

    def from_engine(self, engine):
        players = engine.players
        for id in players:
            player = players[id]
            body = player.body
            # TODO: Modify toyblock3.Pool to accept variable arguments and keywords
            # self.players[id] = Body(body.x, body.y)
            snapshot_body = Body()
            snapshot_body.x = body.x
            snapshot_body.y = body.y
            snapshot_body.vel_x = body.vel_x
            snapshot_body.vel_y = body.vel_y
            self.players[id] = snapshot_body

    def from_diff_data(self, data):
        n_players = int.from_bytes(data[:1], "big")
        if n_players:
            player_data = data[1:body_struct.size*n_players+1]
            for id, x, y, vel_x, vel_y in body_struct.iter_unpack(player_data):
                body = Body()
                body.x = x
                body.y = y
                body.vel_x = vel_x
                body.vel_y = vel_y
                self.players[id] = body
    
    def apply_to_engine(self, engine):
        players = self.players
        for id in self.players:
            engine_player = engine.players.get(id)
            if not engine_player:
                continue
            player = players[id]
            engine_player.body.x = player.x
            engine_player.body.y = player.y
            engine_player.body.vel_x = player.vel_x
            engine_player.body.vel_y = player.vel_y
    
    def reset(self):
        for id in self.players:
            self.players[id].free()
        self.players.clear()

    def borrow(self):
        self._borrowed += 1

    def free(self):
        self._borrowed -= 1
        if self._borrowed:
            return
        super().free() 

    def diff(self, other_snapshot):
        data = bytearray() 
        player_data = bytearray()
        for id in self.players:
            player = self.players[id]
            other_player = other_snapshot.players.get(id)
            if not other_player or player.diff(other_player):
                player_data += body_struct.pack(id, player.x, player.y, player.vel_x, player.vel_y)
        data += int.to_bytes(len(self.players), 1, "big")
        data += player_data
        return data

Snapshot = toyblock3.Pool(SnapshotMixin, MAX_SNAPSHOTS)
    
class PlayerSnapshot_:
    def __init__(self):
        self.ack = False
        self.snapshot = None

    def reset(self):
        self.ack = False
        self.snapshot.free()
        self.snapshot = None

PlayerSnapshot = toyblock3.Pool(PlayerSnapshot_, MAX_SNAPSHOTS*4)
