import toyblock3
from polytanks.engine import AbstractEngine
from .entity import Platform, Player
from . import system
from .system import polytanks_system

class Engine(AbstractEngine):
    def __init__(self, batch, groups):
        pools = {
            "player": toyblock3.Manager(Player, 4, batch, groups),
            "platform": toyblock3.Pool(Platform, 64, batch, groups[0])
        }
        super().__init__(pools)

    def update(self, dt):
        system.input()
        polytanks_system.physics()
        system.sprite()

    def regenerate_id(self):
        pass

    def generate_id(self):
        return 0
