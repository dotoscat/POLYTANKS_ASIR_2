import toyblock3

MAX_SNAPSHOTS = 32*4

class Body_:
    def __init__(self):
        self.x = 0.
        self.y = 0.

    def reset(self):
        self.x = 0.
        self.y = 0.

Body = toyblock3.Pool(Body_, MAX_SNAPSHOTS)

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
