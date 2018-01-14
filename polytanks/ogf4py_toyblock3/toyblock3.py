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

from collections import deque

class Poolable:
    __pool = None
    def free(self):
        if not self.__pool:
            return
        self.__pool.free(self)
    def reset(self):
        raise NotImplementedError("Implement reset for this Poolable")
    @classmethod
    def set_pool(cls, pool):
        cls.__pool = pool

class Pool:
    """Create an pool object with any class that is *Poolable*.
    
    Get an object from this pool just creating an instance. This instance
    has the *free* method.
    
    Example:
    
        .. code-block:: python
        
            class Body(Poolable):
                def __init__(self):
                    self.x = 0
                    self.y = 0
                    
                def reset(self):
                    self.x = 0
                    self.y = 0
        
            body_pool = Pool(Body, 10)

            one = body_pool()
            two = body_pool()
            one.free()
            two.free()
        
    """
    def __init__(self, poolable, n_entities, *args, **kwargs):
        """Create a pool of n_entities with a *poolable* class.

        Parameters:
            poolable (:class:`Poolable`): Any class which inherits from Poolable.
            n_entities (int): Number of entities for this pool
            *args: args for creating the instances.
            **kwargs: kwargs for creating the instances.

        Raises:
            TypeError if the class is not poolable
        """
        if not issubclass(poolable, Poolable):
            raise TypeError("Type passed is not poolable")
        self.entities = deque([poolable(*args, **kwargs) for i in range(n_entities)])
        self.used = deque()
        poolable.set_pool(self)

    def free(self, entity):
        if entity not in self.used:
            return
        entity.reset()
        self.used.remove(entity)
        self.entities.append(entity)
        
    def __call__(self, *args, **kwargs):
        """Return an instance from its pool. None if there is not an avaliable entity."""
        if not self.entities:
            return None
        entity = self.entities.pop()
        self.used.append(entity)
        return entity

class System:
    def __init__(self):
        self._entities = deque()
        self._locked = False
        self._add_entity_list = deque()
        self._remove_entity_list = deque()
        
    @property
    def entities(self):
        """Return the current entities that are in this System."""
        return self._entities
    
    def add_entity(self, entity):
        if self._locked:
            self._add_entity_list.append(entity)
        else:
            self._entities.append(entity)
    
    def remove_entity(self, entity):
        if self._locked:
            self._remove_entity_list.append(entity)
        else:
            self._entities.remove(entity)
    
    def __call__(self):
        """Call the system to compute the entities.
        
        Example:
        
            .. code-block:: python
            
                class PhysicsSystem(toyblock3.System, dt):
                    def __init__(self):
                        super().__init__()
                        self.dt = dt

                    def _update(self, entity):
                        entity.body.update(self.dt)
                        
                physics = PhysicsSystem(STEP)
                physics.add_entity(player)
                
                while not game_over:
                    physics()
        
        """
        if self._locked: return
        entities = self._entities
        update = self._update
        self._locked = True
        for entity in entities:
            update(entity)
        self._locked = False
        while self._remove_entity_list:
            self._entities.remove(self._remove_entity_list.pop())
        while self._add_entity_list:
            self._entities.append(self._add_entity_list.pop())

    def _update(self, entity):
        raise NotImplementedError("Define an _update method for this system.")
