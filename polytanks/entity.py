from ogf4py_toyblock3.component import Body
from . import component

class Player:
    def __init__(self, batch, groups):
        self.input = component.KeyControl() 
        # self.sprite = self.Sprite(batch, groups, 1)
        self.body = Body()
    def reset(self):
        pass

class Platform:
    pass