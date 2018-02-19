import toyblock3
from ogf4py_toyblock3 import system
from . import constants

UNIT = constants.UNIT

class InputSystem(toyblock3.System):
    def _update(self, entity):
        entity.body.vel_x = entity.input.move*UNIT*2.

input = InputSystem()
collision = system.CollisionSystem()
physics = system.PhysicsSystem(constants.FPS)
