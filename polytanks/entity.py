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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.#Copyright (C) 2017  Oscar 'dotoscat' Triano <dotoscat (at) gmail (dot) com>

from ogf4py_toyblock3.component import Body, CollisionRect
from . import collision, component
from .constants import UNIT

class Player:
    def __init__(self):
        self.input = component.Control() 
        self.collisions = []
        self.body = Body()

        feet = CollisionRect(UNIT, UNIT/2.)
        feet.offset = (-UNIT/2, -UNIT/2.)
        feet.type = collision.PLAYER_FEET
        feet.collides_with = collision.PLATFORM

        self.collisions.append(feet)

    def reset(self):
        self.body.x = 0.
        self.body.y = 0.
        self.body.vel_x = 0.
        self.body.vel_y = 0.

class Platform:
    def __init__(self):
        self.collisions = [CollisionRect(UNIT, UNIT/2.)]

        rect = self.collisions[0]
        rect.offset = (-UNIT/2., UNIT/2.)
        rect.type = collision.PLATFORM
    
    def set_geometry(self, x, y, tiles_width):
        collision = self.collisions[0]
        collision.x = x
        collision.y = y
        collision.width = tiles_width*UNIT
