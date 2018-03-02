from itertools import count
import toyblock3
from polytanks.engine import AbstractEngine
from polytanks.entity import Player, Platform
from polytanks.system import input, physics

Player.SYSTEMS = (input, physics)

class Engine(AbstractEngine):
    def __init__(self, n_players, start_id):
        pools = {
            "player": toyblock3.Manager(Player, n_players),
            "platform": toyblock3.Manager(Player, 64)
        }
        super().__init__(pools)
        self.start_id = start_id
        self.id_generator = None
        self.regenerate_id()

    def update(self, dt):
        input()
        physics()

    def generate_id(self):
        return next(self.id_generator)

    def regenerate_id(self):
        self.id_generator = count(self.start_id)
