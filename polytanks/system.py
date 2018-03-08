# Copyright (C) 2018  Oscar 'dotoscat' Triano    <dotoscat (at) gmail (dot) com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import toyblock3
from ogf4py_toyblock3 import system
from .constants import UNIT, FPS
from . import event
from .event import event_manager

class InputSystem(toyblock3.System):
    def __init__(self):
        super().__init__()
        self.jump_event = False
        self.float_event = False
    def _update(self, entity):
        entity.body.vel_x = entity.input.move*UNIT*2.
        # print("input vel y", entity.body.vel_y)
        self.float_event = False
        self.jump_event = False
        if entity.input.jumps and entity.input.touch_floor and not entity.input.jump_pressed:
            entity.body.vel_y = UNIT*3.
            entity.body.has_gravity = True
            entity.input.touch_floor = False
            entity.input.jump_pressed = True
            self.jump_event = True
        elif entity.input.jumps and not entity.input.touch_floor and not entity.input.jump_pressed:
            if entity.body.vel_y < 0.:
                entity.body.vel_y = UNIT
            else:
                entity.body.vel_y += UNIT
            self.float_event = True
        if not entity.input.jumps and entity.input.jump_pressed:
            entity.input.jump_pressed = False

# input = InputSystem()
collision = system.CollisionSystem()
physics = system.PhysicsSystem(FPS, (0., -UNIT*3.))
