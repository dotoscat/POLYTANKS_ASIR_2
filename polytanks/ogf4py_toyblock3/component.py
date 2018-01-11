#  ogf4py
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

from math import fabs

class Body:
    def __init__(self):
        self.x = 0.
        self.y = 0
        self.vel_x = 0.
        self.vel_y = 0.
        self.max_falling_speed = 0.
        self.max_ascending_speed = 0.
        self.has_gravity = False

    def update(self, dt, gravity):
        if self.has_gravity: self.vel_y += gravity*dt
        if self.vel_y < 0. and fabs(self.vel_y) > self.max_falling_speed > 0.:
            self.vel_y = -self.max_falling_speed
        elif self.vel_y > self.max_ascending_speed > 0.:
            self.vel_y = self.max_ascending_speed
        self.x += self.vel_x*dt
        self.y += self.vel_y*dt

    def apply_force(self, dt, x=0., y=0.):
        self.vel_x += x*dt
        self.vel_y += y*dt

class CollisionRect:
    def __init__(self, width, height, x=0., y=0.):
        self.offset = (0., 0.)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = 0
        self.collides_width = 0

    @property
    def right(self):
        return self.x + self.width

    @property
    def top(self):
        return self.y + self.height

    def intersects(self, b):
        if b.y >= self.top: return False    # top
        if b.top <= self.y: return False    # bottom
        if b.right <= self.x: return False  # left
        if b.x >= self.right: return False  # right
        return True

    def __contains__(self, x, y):
        return self.x <= x <= self.right and self.y <= y <= self.top

    def update(self, x, y):
        self.x = x + self.offset[0]
        self.y = y + self.offset[1]
