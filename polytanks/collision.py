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
BULLET = 1 << 3
BLAST_ZONE = 1 << 4
EXPLOSION = 1 << 5

class CollisionMixin:
    """
    This class is mixed with the abstract :class:`AbstractEngine`.
    Then you can override the following callbacks from the class derivated
    from AbstractEngine. Do not forget call super().
    """
    def register_collisions(self):
        collision.register_callbacks(
            (PLAYER_FEET, PLATFORM),
            start=self.player_platform_start,
            end=self.player_platform_end
        )
        collision.register_callbacks(
            (BULLET, PLATFORM),
            start=self.bullet_platform_start
        )
        collision.register_callbacks(
            (BULLET, PLAYER),
            start=self.bullet_player_start
        )
        collision.register_callbacks(
            (PLAYER, BLAST_ZONE),
            end=self.player_blastzone_end
        )
        collision.register_callbacks(
            (BULLET, BLAST_ZONE),
            end=self.bullet_blastzone_end
        )
        collision.register_callbacks(
            (EXPLOSION, PLAYER),
            start=self.explosion_player_start
        )

    def player_platform_start(self, player, platform, player_rect, platform_rect):
        if player.body.vel_y > 0.:
            return
        player.body.y = platform_rect.top + -player_rect.offset[1]-1.
        player.body.vel_y = 0.
        player.body.has_gravity = False
        player.input.touch_floor = True
        print("touch floor")

    def player_platform_end(self, player, platform, player_rect, platform_rect):
        if player.body.vel_y > 0.:
            return
        player.body.has_gravity = True
        player.input.touch_floor = False
        print("player_platform_end")

    def player_blastzone_end(self, player, blastzone, player_rect, blastzone_rect):
        self.respawn_player(player.id)
        print("Player goes kabooooo")

    def bullet_player_start(self, bullet, player, bullet_rect, player_rect):
        print("bullet collides", bullet.info.owner, player.id)
        if bullet.info.owner == player.id:
            return
        self._bullet_explodes(bullet)

    def bullet_platform_start(self, bullet, platform, bullet_rect, platform_rect):
        self._bullet_explodes(bullet)

    def _bullet_explodes(self, bullet):
        y = bullet.body.y
        x = bullet.body.x
        self.add_explosion(x, y, bullet.info.power)
        bullet.free()

    def bullet_blastzone_end(self, bullet, blastzone, bullect_rect, blastzone_rect):
        if not bullet._used:
            return
        print("Bullet freed")
        bullet.free()

    def explosion_player_start(self, explosion, player, explosion_rect, player_rect):
        pass
