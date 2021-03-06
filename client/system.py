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

from math import degrees
import toyblock3
from polytanks.constants import UNIT
import polytanks.system as polytanks_system

class SpritesSystem(toyblock3.System):
    def _update(self, entity):
        body = entity.body
        sprite = entity.sprite
        sprite.x = body.x
        sprite.y = body.y

class InputSystem(polytanks_system.InputSystem):
    def _update(self, entity):
        super()._update(entity)
        cannon_angle = entity.sprite.get_cannon_angle(entity.input.pointer_x, entity.input.pointer_y)
        entity.sprite.cannon.rotation = degrees(cannon_angle)
        entity.input.cannon_angle = cannon_angle

sprite = SpritesSystem()
input = InputSystem()
