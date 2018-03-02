# Copyright (C) 2017  Oscar 'dotoscat' Triano <dotoscat (at) gmail (dot) com>

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
    "..............._....................",
    "....................................",
    "............______..................",
    "......____.........._________.......",
    "....................................",
    "....................................",
    "...______________________________...",
    "....................................",
    "...................................."
]

def load_level(level_info, platform_pool):
    for y, l in enumerate(reversed(level_info)):
        iter_l = iter(l)
        x = 0.
        while True:
            c = next(iter_l, None)
            if c is None:
                break
            if c != '_':
                x += 1.
                continue
            platform = platform_pool()
            # TODO: Implement collision for the platforms
            try:
                platform.sprite.x = x*UNIT
                platform.sprite.y = y*UNIT
            except AttributeError:
                pass
            x += 1.
