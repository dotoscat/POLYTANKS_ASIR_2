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

import toyblock3
from polytanks.constants import UNIT
import polytanks.system as polytanks_system

class SpritesSystem(toyblock3.System):
    def _update(self, entity):
        body = entity.body
        sprite = entity.sprite
        sprite.x = body.x
        sprite.y = body.y

class InputSystem(toyblock3.System):
    def _update(self, entity):
        entity.body.vel_x = entity.input.move*UNIT*2.
        entity.sprite.update_cannon_angle(entity.input.pointer_x, entity.input.pointer_y)

sprite = SpritesSystem()
input = InputSystem()
