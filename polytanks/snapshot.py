import struct
import toyblock3

MAX_SNAPSHOTS = 64*4

class Body_:
    def __init__(self):
        self.x = 0.
        self.y = 0.

    def reset(self):
        self.x = 0.
        self.y = 0.

    def diff(self, body):
        return self.x != body.x or self.y != body.y

Body = toyblock3.Pool(Body_, MAX_SNAPSHOTS*4)

body_struct = struct.Struct("!iff")

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
            self.players[id] = Body(body.x, body.y)

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
        n_players = 0
        for id in self.players:
            player = self.players[id]
            other_player = other_snapshot.players.get(id)
            if not other_player:
                continue
            if player.diff(other_player):
                n_players += 1
                player_data += body_struct.pack(id, player.x, player.y)
        data += int.to_bytes(n_players, 1, "big")
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