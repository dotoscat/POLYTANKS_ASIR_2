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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.#Copyright (C) 2017  Oscar 'dotoscat' Triano <dotoscat (at) gmail (dot) com>

from .collision import CollisionMixin
from . import level

class AbstractEngine(CollisionMixin):
    def __init__(self, pools):
        types = ("player", "platform")
        for t in types:
            if t not in pools:
                raise Exception("{} not found in pools".format(t))
        self.pools = pools
        self.entities = {}
        self.players = {}
        self.register_collisions()

    def load_level(self):
        level.load_level(level.basic, self.pools["platform"])
    
    def regenerate_id(self):
        raise NotImplementedError

    def add_player(self, id=None):
        player_pool = self.pools.get("player")
        player = player_pool()
        if player is None:
            return 
        id = id if isinstance(id, int) else self.generate_id()
        self.entities[id] = player
        self.players[id] = player
        return (id, player)

    def remove(self, id):
        entity = self.entities.get(id)
        if not entity:
            return False
        entity.free()
        del self.entities[id]
        return True

    def remove_player(self, id):
        removed = self.remove(id)
        if removed:
            del self.players[id]

    def update(self, dt):
        raise NotImplementedError

    def generate_id(self):
        raise NotImplementedError
