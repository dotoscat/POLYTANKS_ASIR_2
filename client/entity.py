import pyglet
import polytanks.entity as pentity
from . import assets
from .component import TankGraphic
from . import system

class Platform(pentity.Platform):
    SYSTEMS = ()
    def __init__(self, batch, group):
        self.sprite = pyglet.sprite.Sprite(assets.images["platform"], batch=batch, group=group)
    def reset(self):
        pass

class Player(pentity.Player):
    SYSTEMS = (system.input, system.polytanks_system.physics, system.sprite)
    def __init__(self, batch, groups):
        super.__init__()
        self.sprite = TankGraphic(batch, groups, 1)
    def reset(self):
        pass
