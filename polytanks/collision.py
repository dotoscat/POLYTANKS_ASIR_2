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

from .system import collision

PLAYER = 1
PLATFORM = 1 << 1
PLAYER_FEET = 1 << 2

class CollisionMixin:
    def register_collisions(self):
        collision.register_callbacks(
            (PLAYER_FEET, PLATFORM),
            self.player_platform_start,
            self.player_platform,
            self.player_platform_end
        )

    def player_platform_start(self, player, platform, player_rect, platform_rect):
        # print("start", player, platform, player_rect, platform_rect)
        print("start")
        player.body.y = platform_rect.top + -player_rect.offset[1]-1.
        player.body.vel_y = 0.
        player.body.has_gravity = False
        player.input.touch_floor = True

    def player_platform(self, player, platform, player_rect, platform_rect):
        # print(player_rect.x, player_rect.y, platform_rect.x, platform_rect.y)
        # print("touch_floor, has_gravity: ", player.input.touch_floor, player.body.has_gravity, player.body.vel_y)
        # print("collision vel y", player.body.vel_y)
        print("during")
        # print("player y, height, top:", player_rect.y, player_rect.height, player_rect.top)
        #print("platform y, height, top:", platform_rect.y, platform_rect.height, platform_rect.top)

    def player_platform_end(self, player, platform, player_rect, platform_rect):
        # print("end", player, platform, player_rect, platform_rect)
        print("end")
        # player.body.has_gravity = True
        # player.input.touch_floor = False
        player.body.has_gravity = False
        player.input.touch_floor = True
