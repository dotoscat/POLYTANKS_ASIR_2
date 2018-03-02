from ogf4py_toyblock3.component import Body
from . import component

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
    pass