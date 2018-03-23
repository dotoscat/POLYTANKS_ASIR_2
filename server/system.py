# Copyright (C) 2018  Oscar 'dotoscat' Triano <dotoscat (at) gmail (dot) com>

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

from math import cos, sin, degrees
import warnings
from polytanks import system
from polytanks import event
from polytanks.event import event_manager
from polytanks.constants import CANNON_JOINT, CANNON_LENGTH, BULLET_SPEED

class InputSystem(system.InputSystem):
    def __init__(self):
        super().__init__()
        self.engine = None
    def _update(self, entity):
        shoot_time = entity.input.shoot_time
        super()._update(entity)
        if self.jump_event:
            event_manager.add_player_event(event.PLAYER_JUMPS, entity.id)
            print(entity, "jumps")
        if self.float_event:
            event_manager.add_player_event(event.PLAYER_FLOATS, entity.id)
            print(entity, "floats") 
        if self.shot_event:
            if not self.engine:
                warnings.warn("'engine' attribute for the system is None.")
            body = entity.body
            if shoot_time > 0.:
                gravity = True
                power = 5
                speed = BULLET_SPEED/4.
            elif shoot_time > 1.:
                gravity = True
                power = 10
                speed = BULLET_SPEED/2.
            elif shoot_time > 2.:
                gravity = False
                power = 30
                speed = BULLET_SPEED

            id, bullet = self.engine.add_bullet(
                entity.id, body.x, body.y,
                entity.input.cannon_angle, power, speed, gravity)
            event_manager.add_shot_event(entity.id, body.x, body.y, entity.input.cannon_angle, power, id)
            print("bullet:", id, bullet.body.x, bullet.body.y, "speed", speed, "power", power)

input = InputSystem()
