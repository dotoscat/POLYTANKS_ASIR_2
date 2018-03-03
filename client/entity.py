import pyglet
import polytanks.entity as pentity
from . import assets
from .component import TankGraphic, PlatformSprite
from . import system

class Platform(pentity.Platform):
    SYSTEMS = ()
    def __init__(self, batch, group):
        super().__init__()
        self.sprite = None
        self.batch = batch
        self.group = group

    def reset(self):
        self.sprite = None

    def set_geometry(self, x, y, tiles_width):
        super().set_geometry(x, y, tiles_width)
        self.sprite = PlatformSprite(
            assets.images["platform"], tiles_width,
            x=x, y=y, batch=self.batch, group=self.group)

class Player(pentity.Player):
    SYSTEMS = (system.input, system.polytanks_system.physics, system.sprite)
    def __init__(self, batch, groups):
        super().__init__()
        self.sprite = TankGraphic(batch, groups, 1)
    def reset(self):
        pass
