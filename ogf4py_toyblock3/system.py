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
    def __init__(self, iterations=10):
        super().__init__()
        self.callbacks = {}
        self._collisions = {}
        self.iterations = iterations

    def _update(self, entity):
        collisions = getattr(entity, "collisions")
        if not collisions:
            return
        if not collisions.active:
            return
        for rect, other_entity in product(collisions, self.entities):
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
                # TODO: pass the whole entity to method
                if not self.check_collision_body_body(entity, other_entity, rect, other_rect):
                # if not rect.intersects(other_rect):
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

    def body_steps(self, body):
        step_x = (body.x - body._last_x)/self.iterations
        step_y = (body.y - body._last_y)/self.iterations
        
        x = body._last_x
        y = body._last_y

        for _ in range(self.iterations+1):
            yield (x, y)
            x += step_x
            y += step_y

    def check_collision_body_body(self, entity1, entity2, body1_rect, body2_rect):
        body1 = getattr(entity1, "body")
        body2 = getattr(entity2, "body")
        if not body1 or not body2:
            return False
        body1_x_step = (body1.x - body1._last_x) / self.iterations 
        body1_y_step = (body1.y - body1._last_y) / self.iterations
        body2_x_step = (body2.x - body2._last_x) / self.iterations 
        body2_y_step = (body2.y - body2._last_y) / self.iterations 
        body1_x = body1._last_x
        body1_y = body1._last_y
        body2_x = body2._last_x
        body2_y = body2._last_y
        for _ in range(self.iterations):
            body1_rect.update(body1_x, body1_y)
            body2_rect.update(body2_x, body2_y)
            if body1_rect.intersects(body2_rect):
                return True
            body1_x += body1_x_step
            body1_y += body1_y_step
            body2_x += body2_x_step
            body2_y += body2_y_step
        return False

    def register_callbacks(self, pair, start=None, during=None, end=None):
        """
        Register up to 3 collision events for a pair.

        When a collisions starts the *during* event will be triggered too.

        All the callbacks have the following signature:
            callback(first_entity, second_entity, first_entity_rect, second_entity_rect)

        Parameters:
            pair (tuple): A tuple with two integers inside it.
            start (callable): A callable when the collision starts.
            during (callable): This will be called during the collision.
            end (callable): This will be triggered when the collision ends.

        Example:
            PLAYER = 1
            BULLET = 2
            my_collision = CollisionSystem()
            # ... set up
            player.collisions[0].type = PLAYER
            player.collisions[0].collides_with = BULLET
            bullet.collisions[0].type = BULLET

            def player_bullet(player, bullet, player_rect, bullet_rect):
                player.hit()
                bullet.free()

            my_collision.register_callbacks(
                (PLAYER, BULLET),
                start=player_bullet
            )
        """
        callbacks = CollisionSystem.Callbacks(start, during, end)
        self.callbacks[pair] = callbacks 
