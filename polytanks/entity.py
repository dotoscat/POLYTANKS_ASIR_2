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

from ogf4py_toyblock3.component import Body, CollisionRect, Collisions
from . import collision, component, system
from .constants import UNIT, HALF_UNIT, WIDTH, HEIGHT

class Blastzone:
    SYSTEMS = (system.collision,)
    def __init__(self):
        self.collisions = Collisions()
        self.collisions.active = False

        bottom = CollisionRect(WIDTH+UNIT*4, UNIT*2, x=-UNIT*2, y=-UNIT*2)
        bottom.type = collision.BLAST_ZONE
        
        self.collisions.append(bottom)

class Player:
    def __init__(self, input_component=component.Control):
        self.id = 0
        self.input = input_component()
        self.collisions = Collisions()
        self.body = Body()
        self.info = component.Info()

        feet = CollisionRect(UNIT, 2)
        feet.offset = (-UNIT/2, -UNIT/2.)
        feet.type = collision.PLAYER_FEET
        feet.collides_with = collision.PLATFORM | collision.BLAST_ZONE

        self.collisions.append(feet)

    def reset(self):
        self.id = 0
        self.body.reset()
        self.input.touch_floor = False

class Platform:
    def __init__(self):
        self.collisions = Collisions( (CollisionRect(UNIT, UNIT/4.),) )

        rect = self.collisions[0]
        rect.type = collision.PLATFORM
        rect.active = False

    def set_geometry(self, x, y, tiles_width):
        collision = self.collisions[0]
        collision.x = x
        collision.y = y + UNIT - collision.height
        collision.width = tiles_width*UNIT

class Bullet:
    def __init__(self):
        self.body = Body()
        self.body.has_gravity = True
        self.collisions = Collisions()
        self.owner = 0

        width = HALF_UNIT
        height = HALF_UNIT

        rect = CollisionRect(width, height)
        rect.offset = (-width/2., -height/2.)
        rect.type = collision.BULLET
        rect.collides_with = collision.PLATFORM | collision.PLAYER | collision.BLAST_ZONE

        self.collisions.append(rect)

    def reset(self):
        self.body.reset()
        self.owner = 0
