import toyblock3

class Body_:
    def __init__(self):
        self.x = 0.
        self.y = 0.

    def reset(self):
        self.x = 0.
        self.y = 0.

Body = toyblock3.Pool(Body_, 64)

class Snapshot_:
    def __init__(self):
        self.players = {}

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

Snapshot = toyblock3.Pool(Snapshot_, 64)
    
class PlayerSnapshot_:
    def __init__(self):
        self.ack = False
        self.snapshot = None

    def reset(self):
        self.ack = False
        self.snapshot = None

PlayerSnapshot = toyblock3.Pool(PlayerSnapshot_, 256)
