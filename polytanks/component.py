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

from struct import Struct

_control_struct = Struct("!f??f") 

class Control:
    def __init__(self):
        self.move = 0.
        self.pointer_x = 0.
        self.pointer_y = 0.
        self.cannon_angle = 0.
        self.touch_floor = False
        self.jumps = False
        self.jump_pressed = False
        self.shoots = False
        self.shoot_time = 0.

    def from_bytes(self, data):
        self.move, self.jumps, self.shoots, self.cannon_angle = _control_struct.unpack(data)

    def __bytes__(self):
        return _control_struct.pack(self.move, self.jumps, self.shoots, self.cannon_angle)
    
class PlayerInfo:
    def __init__(self):
        self.damage = 0
        self.touched_floor = False

class BulletInfo:
    def __init__(self):
        self.owner = 0
        self.power = 0

    def reset(self):
        self.owner = 0
        self.power = 0