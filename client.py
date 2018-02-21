import sys
import os
import pyglet
from ogf4py.director import Director
sys.path.insert(0, os.path.abspath(__package__))
from polytanks.constants import WIDTH, HEIGHT
from client.client import Client
from client.scene import Screen, Main

if __name__ == "__main__":
    ADDRESS = ("127.0.0.1", 1337)
    client = Client()
    director = Director(width=WIDTH, height=HEIGHT)
    # director.scene = Main(client, ADDRESS)
    director.scene = Screen(client)
    pyglet.app.run()
