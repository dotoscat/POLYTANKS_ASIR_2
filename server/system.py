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

from polytanks import system
from polytanks import event
from polytanks.event import event_manager

class InputSystem(system.InputSystem):
    def _update(self, entity):
        super()._update(entity)
        if self.jump_event:
            event_manager.add_player_event(event.PLAYER_JUMPS, entity.id)
            print(entity, "jumps")
        if self.float_event:
            event_manager.add_player_event(event.PLAYER_FLOATS, entity.id)
            print(entity, "floats") 

input = InputSystem()
