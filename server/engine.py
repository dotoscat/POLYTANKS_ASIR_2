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

from itertools import count
import toyblock3
from polytanks.engine import AbstractEngine
from .entity import Player, Platform, Bullet, Explosion, Powerup
from polytanks.system import physics, collision, lifetime
from .system import input
from polytanks.event import event_manager
from polytanks import event
from polytanks.constants import UNIT

class Engine(AbstractEngine):
    def __init__(self, n_players, start_id):
        pools = {
            "player": toyblock3.Manager(Player, n_players),
            "platform": toyblock3.Manager(Platform, 64),
            "bullet": toyblock3.Manager(Bullet, 128),
            "explosion": toyblock3.Manager(Explosion, 128),
            "powerup": toyblock3.Manager(Powerup, 32)
        }
        super().__init__(pools)
        self.start_id = start_id
        self.id_generator = None
        self.regenerate_id()

    def update(self, dt):
        lifetime()
        input()
        physics()
        collision()

    def generate_id(self):
        return next(self.id_generator)

    def regenerate_id(self):
        self.id_generator = count(self.start_id)

    def player_platform_start(self, player, platform, player_rect, platform_rect):
        super().player_platform_start(player, platform, player_rect, platform_rect)
        event_manager.add_player_event(event.PLAYER_TOUCHES_FLOOR, player.id)
        # print("events", len(event_manager.events))

    def explosion_player_start(self, explosion, player, explosion_rect, player_rect):
        super().explosion_player_start(explosion, player, explosion_rect, player_rect)
        player.info.damage += explosion.power
        knockback = UNIT*(player.info.damage/10.)
        player.body.vel_y = knockback if knockback >= UNIT else UNIT
        hitstun = 0.25 if knockback <= UNIT else 1.
        player.info.hitstun = hitstun
        if player.input.touch_floor:
            player.body.has_gravity = True
        event_manager.add_player_hurt(player.id, player.info.damage)

    def powerup_player(self, powerup, player, powerup_rect, player_rect):
        print("player", player, "picks up", powerup.effect)
        if callable(powerup.effect):
            powerup.effect(player)
        powerup.free()
