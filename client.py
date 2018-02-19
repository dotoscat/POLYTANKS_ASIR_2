import sys
import os
sys.path.insert(0, os.path.abspath(__package__))
import pyglet
from pyglet.window import key
import toyblock3
from ogf4py.director import Director
from ogf4py.scene import Scene
from ogf4py_toyblock3 import component, system 
from polytanks import assets, level, protocol
from polytanks.constants import WIDTH, HEIGHT, UNIT
import client.client
from client.client import Client
from client.scene import Main

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

# TODO: inherit prom polytanks.entity.Player
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

# TODO: inherit prom polytanks.entity.Platform
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
    director.scene = Main(client, ADDRESS)
    pyglet.app.run()
