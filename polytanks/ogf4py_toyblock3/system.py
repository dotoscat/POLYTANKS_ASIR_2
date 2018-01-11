#  Copyright (C) 2018 Oscar 'dotoscat' Triano

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.

#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from . import toyblock3

class PhysicsSystem(toyblock3.System):
    def _update(self, entity, dt, gravity):
        entity.body.update(dt, gravity)

class CollisionSystem(toyblock3.System):
    def __init__(self):
        super().__init__()
        self.callbacks = {}

    def _update(self, entity):
        pass

    def register_callback(self, pair):
        def _register_callback(f):
            self.callbacks[pair] = f
            return f
        return _register_callback
    