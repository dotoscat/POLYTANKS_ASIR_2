#  ogf4py_toyblock 
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

from collections import namedtuple
from itertools import product
import toyblock3

class PhysicsSystem(toyblock3.System):
    """Basic system for upgrade body's position, apply gravity and so.

    This system will look at the *body* attribute of the entity which is a Body component.

    If the entity has the *collision* attribute, which is a collection of CollisionRect, then
    proceed to update them once the body is updated.

    Example:

        .. code-block:: python

            my_system = PhysicsSystem(0.016, (0, -10.))

            # add some entities
            my_system.add_entity(asteroid1)
            my_system.add_entity(player)
            while not game_over:
                my_system()
    """
    def __init__(self, dt, gravity=(0., 0.)):
        super().__init__()
        self.dt = dt
        self.gravity = gravity

    def _update(self, entity):
        entity.body.update(self.dt, self.gravity)
        collisions = getattr(entity, "collisions", None)
        if collisions:
            x = entity.body.x
            y = entity.body.y
            for rect in collisions:
                rect.update(x, y)

class CollisionSystem(toyblock3.System):
    """System for collision detection and responses.

    This system will look at the member *collisions*, which is sequence
    of :class:`CollisionRect`.

    """
    Callbacks = namedtuple("Callbacks", "start during end")
    def __init__(self):
        super().__init__()
        self.callbacks = {}
        self._collisions = {}

    def _update(self, entity):
        for rect, other_entity in product(entity.collisions, self.entities):
            if not rect.collides_with:
                continue
            if entity is other_entity:
                continue
            for other_rect in other_entity.collisions:
                if rect.collides_with & other_rect.type != other_rect.type:
                    continue
                pair = (rect, other_rect)
                callbacks = self.callbacks.get((rect.type, other_rect.type))
                if not callbacks:
                    continue
                if not rect.intersects(other_rect):
                    if pair in self._collisions and callable(callbacks.end):
                        callbacks.end(entity, other_entity, rect, other_rect)
                        del self._collisions[pair]
                    continue
                if pair not in self._collisions:
                    self._collisions[pair] = callbacks
                    if callable(callbacks.start):
                        callbacks.start(entity, other_entity, rect, other_rect)
                if callable(callbacks.during):
                    callbacks.during(entity, other_entity, rect, other_rect)

    def register_callback(self, pair):
        """This is a decorator where you define a callback.
        
        The second type of the CollisionRect must have set the flags *collides_with* with the first type.

        The callback has the following signature callback(first_entity, second_entity) 

        Example:

            PLAYER = 1
            BULLET = 2
            my_collision = CollisionSystem()
            # ... set up
            player.collisions[0].type = PLAYER
            player.collisions[0].collides_with = BULLET
            bullet.collisions[0].type = BULLET
            @my_collision.register_callback((PLAYER, BULLET))
            def player_bullet(player, bullet):
                player.hit()
                bullet.free()

        Parameters:
            pair (tuple): pair of two element where you set two collision types for the callback.
        """
        def _register_callback(f):
            self.callbacks[pair] = f
            return f
        return _register_callback
    
    def register_callbacks(self, pair, start=None, during=None, end=None):
        callbacks = CollisionSystem.Callbacks(start, during, end)
        self.callbacks[pair] = callbacks 
