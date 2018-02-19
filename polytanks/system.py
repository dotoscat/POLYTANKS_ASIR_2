import toyblock3
from . import constants
UNIT = constants.UNIT

class InputSystem(toyblock3.System):
    def _update(self, entity):
        entity.body.vel_x = entity.input.move*UNIT*2.
