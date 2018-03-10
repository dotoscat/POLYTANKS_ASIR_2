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

import warnings
from polytanks import system
from polytanks import event
from polytanks.event import event_manager

class InputSystem(system.InputSystem):
    def __init__(self):
        super().__init__()
        self.engine = None
    def _update(self, entity):
        super()._update(entity)
        if self.jump_event:
            event_manager.add_player_event(event.PLAYER_JUMPS, entity.id)
            print(entity, "jumps")
        if self.float_event:
            event_manager.add_player_event(event.PLAYER_FLOATS, entity.id)
            # print(entity, "floats") 
        if self.shot_event:
            if not self.engine:
                warnings.warn("'engine' attribute for the system is None.")
            id, bullet = self.engine.add_bullet()
            event_manager.add_player_make_event(event.PLAYER_SHOOTS, entity.id, id)
            bullet.body.x = entity.body.x
            bullet.body.y = entity.body.y
            print("bullet", bullet.body.x, bullet.body.y)
            # engine.create_bullet and so

input = InputSystem()
