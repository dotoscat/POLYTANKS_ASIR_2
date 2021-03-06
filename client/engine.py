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
from polytanks.engine import AbstractEngine
from .entity import Platform, Player, Bullet, Explosion, Powerup
from . import system
from .system import polytanks_system

class Engine(AbstractEngine):
    def __init__(self, batch, groups):
        pools = {
            "player": toyblock3.Manager(Player, 4, batch, groups),
            "platform": toyblock3.Manager(Platform, 64, batch, groups[0]),
            "bullet": toyblock3.Manager(Bullet, 128, batch, groups[2]),
            "explosion": toyblock3.Manager(Explosion, 128, batch, groups[3]),
            "powerup": toyblock3.Manager(Powerup, 32, batch, groups[3])
        }
        super().__init__(pools)

    def update(self, dt):
        polytanks_system.lifetime()
        system.input()
        polytanks_system.physics()
        polytanks_system.collision()
        system.sprite()

    def regenerate_id(self):
        pass

    def generate_id(self):
        return 0
    