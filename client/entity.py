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

import pyglet
import polytanks.entity as pentity
from . import assets
from .component import TankGraphic, PlatformSprite, Control
from . import system

class Platform(pentity.Platform):
    SYSTEMS = (system.polytanks_system.collision,)
    def __init__(self, batch, group):
        super().__init__()
        self.sprite = None
        self.batch = batch
        self.group = group

    def reset(self):
        self.sprite = None

    def set_geometry(self, x, y, tiles_width):
        super().set_geometry(x, y, tiles_width)
        self.sprite = PlatformSprite(
            assets.images["platform"], tiles_width,
            x=x, y=y, batch=self.batch, group=self.group)

class Player(pentity.Player):
    SYSTEMS = (system.input, system.polytanks_system.physics, system.polytanks_system.collision, system.sprite)
    def __init__(self, batch, groups):
        super().__init__(input_component=Control)
        self.sprite = TankGraphic(batch, groups, 1)
    def reset(self):
        pass

class Bullet(pentity.Bullet):
    SYSTEMS = (system.polytanks_system.physics, system.polytanks_system.collision, system.sprite)
    def __init__(self, batch, group):
        super().__init__()
        self.sprite = pyglet.sprite.Sprite(assets.images["bullet"], batch=batch, group=group)
