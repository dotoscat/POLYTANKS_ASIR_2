import sys
import os
from math import atan2, degrees
import pyglet
from pyglet.window import key
import toyblock3
from polytanks.ogf4py.director import Director
from polytanks.ogf4py.scene import Scene
from polytanks.ogf4py_toyblock3 import component, system 
from polytanks import assets, level, protocol
from polytanks.constants import WIDTH, HEIGHT, UNIT
import client.client
from client.client import Client

sys.path.insert(0, os.path.abspath(__package__))

class KeyControl:
    def __init__(self):
        self.left_keys = (key.A, key.LEFT)
        self.right_keys = (key.D, key.RIGHT) 
        self.move = 0.
        self.pointer_x = 0.
        self.pointer_y = 0.

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

class InputSystem(toyblock3.System):
    def _update(self, entity):
        entity.body.vel_x = entity.input.move*UNIT*2.
        entity.sprite.update_cannon_angle(entity.input.pointer_x, entity.input.pointer_y)

input_system = InputSystem()

class SpritesSystem(toyblock3.System):
    def _update(self, entity):
        body = entity.body
        sprite = entity.sprite
        sprite.x = body.x
        sprite.y = body.y

sprites_system = SpritesSystem()
physics_system = system.PhysicsSystem(1./60.)

class Player:
    SYSTEMS = (input_system, physics_system, sprites_system)
    Input = KeyControl
    Body = component.Body
    Sprite = TankGraphic
    def __init__(self, batch, groups):
        self.input = self.Input() 
        self.sprite = self.Sprite(batch, groups, 1)
        self.body = component.Body()
    def reset(self):
        pass

class Platform:
    SYSTEMS = ()
    Sprite = pyglet.sprite.Sprite
    def __init__(self, batch, group):
        self.sprite = self.Sprite(assets.images["platform"], batch=batch, group=group)
    def reset(self):
        pass

if __name__ == "__main__":
    ADDRESS = ("127.0.0.1", 1337)
    client = Client()
    #client.connect_to_server(ADDRESS)
    #print("connected", client.connected)
    #client.disconnect_from_server()
    director = Director(width=WIDTH, height=HEIGHT)
    director.scene = Main(client)
    pyglet.app.run()
