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

class Powerup:
    def __init__(self):
        self.body = Body()
        self.collisions = Collisions()
        rect = CollisionRect(UNIT, UNIT)
        rect.offset = (-HALF_UNIT, -HALF_UNIT)
        rect.type = collision.POWERUP
        rect.collides_with = collision.PLAYER
        self.collisions.append(rect)

    def reset(self):
        self.body.x = -77
        self.body.y = -77

class Explosion:
    def __init__(self):
        self.lifetime = 0.
        self.body = Body()
        self.owner = 0
        self.power = 0.
        self.collisions = Collisions()
        blast = CollisionRect(UNIT, UNIT)
        blast.offset = -UNIT/2., -UNIT/2.
        blast.type = collision.EXPLOSION
        blast.collides_with = collision.PLAYER
        self.collisions.append(blast)

    def reset(self):
        pass

class Blastzone:
    SYSTEMS = (system.collision,)
    def __init__(self):
        self.collisions = Collisions()
        self.collisions.active = False

        zone = CollisionRect(WIDTH+UNIT*4., HEIGHT+UNIT*4., x=-UNIT*2., y=-UNIT*2.)
        zone.type = collision.BLAST_ZONE
        
        self.collisions.append(zone)

class Player:
    def __init__(self, input_component=component.Control):
        self.id = 0
        self.input = input_component()
        self.collisions = Collisions()
        self.body = Body()
        self.body.has_gravity = True
        self.info = component.PlayerInfo()

        feet = CollisionRect(UNIT, 2)
        feet.offset = (-UNIT/2, -UNIT/2.)
        feet.type = collision.PLAYER_FEET
        feet.collides_with = collision.PLATFORM

        self.collisions.append(feet)

        body_rect = CollisionRect(UNIT, UNIT)
        body_rect.offset = (-UNIT/2., -UNIT/2.)
        body_rect.type = collision.PLAYER
        body_rect.collides_with = collision.BLAST_ZONE

        self.collisions.append(body_rect)

    def reset(self):
        self.id = 0
        self.body.reset()
        self.input.touch_floor = False

class Platform:
    def __init__(self):
        self.collisions = Collisions( (CollisionRect(UNIT, UNIT/4.),) )
        self.collisions.active = False

        rect = self.collisions[0]
        rect.type = collision.PLATFORM

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
        self.info = component.BulletInfo()

        width = HALF_UNIT
        height = HALF_UNIT

        rect = CollisionRect(width, height)
        rect.offset = (-width/2., -height/2.)
        rect.type = collision.BULLET
        rect.collides_with = collision.PLATFORM | collision.PLAYER | collision.BLAST_ZONE

        self.collisions.append(rect)

    def reset(self):
        self.body.reset()
        self.info.reset()
