import sys
import os
from ogf4py.director import Director
sys.path.insert(0, os.path.abspath(__package__))
from polytanks.constants import WIDTH, HEIGHT
import client.client
from client.client import Client
from client.scene import Main

input_system = InputSystem()
sprites_system = SpritesSystem()
physics_system = system.PhysicsSystem(1./60.)

if __name__ == "__main__":
    ADDRESS = ("127.0.0.1", 1337)
    client = Client()
    director = Director(width=WIDTH, height=HEIGHT)
    director.scene = Main(client, ADDRESS)
    pyglet.app.run()
