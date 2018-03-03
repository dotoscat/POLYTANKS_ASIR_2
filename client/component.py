from math import atan2, degrees
import pyglet
from pyglet.window import key
from . import assets
from polytanks import component
from polytanks.constants import UNIT

component.Control.left_keys = (key.A, key.LEFT)
component.Control.right_keys = (key.D, key.RIGHT) 

class PlatformSprite:
    def __init__(self, tile, times, x=0., y=0., batch=None, group=None):
        self.sprites = []
        for i in range(times):
            self.sprites.append(
                pyglet.sprite.Sprite(tile, x=x + i*UNIT, y=y, batch=batch, group=group)
            )

    def __del__(self):
        for sprite in self.sprites:
            sprite.delete()

class TankGraphic:
    def __init__(self, batch, groups, group_start):
       self.base = pyglet.sprite.Sprite(assets.images["tank-base"], batch=batch, group=groups[group_start])
       self.cannon = pyglet.sprite.Sprite(assets.images["tank-cannon"], batch=batch, group=groups[group_start - 1])
       self.cannon_offset = (0., 4.)
       self._update()

    @property
    def x(self):
        return self.base.x

    @x.setter
    def x(self, value):
        self.base.x = value
        self._update()
        
    @property
    def y(self):
        return self.base.y

    @y.setter
    def y(self, value):
        self.base.y = value
        self._update()

    def _update(self):
        self.cannon.x = self.base.x + self.cannon_offset[0]
        self.cannon.y = self.base.y + self.cannon_offset[1]

    def update_cannon_angle(self, x, y):
        angle = atan2(y - self.cannon.y, x - self.cannon.x)
        self.cannon.rotation = degrees(-angle)
