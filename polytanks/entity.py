from ogf4py_toyblock3.component import Body
from . import component

class Player:
    def __init__(self):
        self.input = component.Control() 
        self.body = Body()
    def reset(self):
        pass

class Platform:
    pass