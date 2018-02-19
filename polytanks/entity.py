from ogf4py_toyblock3.component import Body
from . import component

class Player:
    SYSTEMS = (input_system, physics_system, sprites_system)
    Input = component.KeyControl
    Body = Body
    # Sprite = TankGraphic
    def __init__(self, batch, groups):
        self.input = component.KeyControl() 
        # self.sprite = self.Sprite(batch, groups, 1)
        self.body = Body()
    def reset(self):
        pass

class Platform:
    pass