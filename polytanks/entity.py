from ogf4py_toyblock3.component import Body, CollisionRect
from . import component
from .constants import UNIT

class Player:
    def __init__(self):
        self.input = component.Control() 
        self.body = Body()
    def reset(self):
        self.body.x = 0.
        self.body.y = 0.
        self.body.vel_x = 0.
        self.body.vel_y = 0.

class Platform:
    def __init__(self):
        self.collisions = [CollisionRect(0., UNIT)]
    
    def set_geometry(self, x, y, tiles_width):
        collision = self.collisions[0]
        collision.x = x
        collision.y = y
        collision.width = tiles_width*UNIT
