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

from .constants import UNIT

basic = [
    "....................................",
    "....................................",
    "....................................",
    "....................................",
    "....................................",
    "....................................",
    "...-...--..---......................",
    "....................................",
    "...................................."
]

class Area:
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.tiles = 1
        self.width = 0.
        self.height = 0.

def load_level(level_info, platform_pool):
    area = None
    for y, l in enumerate(reversed(level_info)):
        iter_l = iter(l)
        x = 0.
        while True:
            c = next(iter_l, None)
            if c is None:
                break
            if c == '.' and area:
                print("platform size", area.x, area.y, area.tiles)
                platform = platform_pool()
                platform.set_geometry(area.x*UNIT, area.y*UNIT, area.tiles)
                area = None
                # create platform
            elif c in ('-', '_'):
                if not area:
                    area = Area() 
                    area.x = x
                    area.y = y
                else:
                    area.tiles += 1
            x += 1.
