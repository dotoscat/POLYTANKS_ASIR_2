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

import unittest
import toyblock3
from polytanks.ogf4py_toyblock3 import system, component

class Entity:
    Body = component.Body
    def __init__(self):
        self.body = self.Body()

class SystemTest(unittest.TestCase):
    def setUp(self):
        self.entity = Entity()
        self.physics = system.PhysicsSystem(1., 0.)
        self.physics.add_entity(self.entity)

    def test_Physics_nocollision(self):
        entity = self.entity
        entity.body.vel_x = 16
        entity.body.vel_y = 16
        self.physics()
        self.assertTrue(entity.body.x >= 16., "Move x")
        self.assertTrue(entity.body.y >= 16., "Move y")

    def test_Physics_collision(self):
        entity = self.entity
        entity.body.vel_x = 16.
        entity.collisions = []
        one = component.CollisionRect(32., 32.)
        one.x = 1.
        one.y = 1.
        self.assertEqual(one.top, 33., "top")
        self.assertEqual(one.right, 33., "right")
        two = component.CollisionRect(8., 8.)
        two.offset = (-4, 0.)
        entity.collisions.append(one)
        entity.collisions.append(two)
        self.physics()
        self.assertEqual(one.x, 16., "one x")
        self.assertEqual(two.x, 16. + -4., "two x with offset")
    
    def test_CollisionSystem_collides(self):
        ONE = 1
        TWO = 2
        entity = self.entity
        entity.collisions = []
        entity.collisions.append(component.CollisionRect(32., 32.))
        entity.collisions[0].type = ONE

        other_entity = Entity()
        other_entity.collisions = [component.CollisionRect(32., 32.)]
        other_entity.collisions[0].type = TWO        
        other_entity.collisions[0].collides_with = ONE        
        other_entity.done = False
        collisions = system.CollisionSystem()
        collisions.add_entity(entity)
        collisions.add_entity(other_entity)
        @collisions.register_callback((ONE, TWO))
        def test_collision(entity, other_entity):
            other_entity.done = True 

        self.physics()
        collisions()
        self.assertTrue(other_entity.done, "Collision callback not called")

class PoolTest(unittest.TestCase):

    def test_pool(self):
        class A:
            def __init__(self, n=7):
                self.n = n
            def reset(self):
                self.n = 7
            
        A_pool = toyblock3.Pool(A, 8)
        self.assertEqual(len(A_pool.entities), 8, "There is not 8 entities in pool.")
        a = A_pool()
        # self.assertEqual(type(a), A, "instance is not an instance of A.")
        self.assertEqual(len(A_pool.entities), 7, "instance not poped from pool.")
        a.n = 12
        a.free()
        self.assertEqual(len(A_pool.entities), 8, "'a' is not freed.")
        a = A_pool()
        self.assertEqual(a.n, 7, "a reset has not been called")
