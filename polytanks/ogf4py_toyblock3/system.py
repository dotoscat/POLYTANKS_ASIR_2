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
    """Basic system for upgrade body's position, apply gravity and so.

    This system will look at the *body* attribute of the entity which is a Body component.

    When your call the system pass a *dt* and a *gravity* (vertical acceleration)

    If the entity has the *collision* attribute, which is a collection of CollisionRect, then
    proceed to update them once the body is updated.

    Example:

        .. code-block:: python

            my_system = PhysicsSystem()
            # add some entities
            while True:
                my_system(0.016, -10.)
    """
    def _update(self, entity, dt, gravity):
        entity.body.update(dt, gravity)
        collision = getattr(entity, "collision", None)
        if collision:
            x = entity.body.x
            y = entity.body.y
            for rect in collision:
                rect.update(x, y)

class CollisionSystem(toyblock3.System):
    """System for collision detection and responses.

    This system will look at the member *collisions*, which is sequence
    of :class:`CollisionRect`.

    """
    def __init__(self):
        super().__init__()
        self.callbacks = {}

    def _update(self, entity)
        return 
        entity_collision = entity.collision
        for an_entity in self.entities:
            if entity is an_entity: continue
            if (entity_collision.type & an_entity.collision.collides_with 
                != entity_collision.type):
                continue
            for an_entity_rect in an_entity.collision:
                if not entity_collision.intersects(an_entity_rect):
                    continue
                

    def register_callback(self, pair):
        def _register_callback(f):
            self.callbacks[pair] = f
            return f
        return _register_callback
    