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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random

class Status:
    RUNNING = 0
    GAMEOVER = 1
    READY = 2

class AbstractGameMode:
    def __init__(self, server, engine, ready_time=5, running_time=10, gameover_time=3):
        self.server = server
        self.engine = engine
        self.GAMEOVER_TIME = gameover_time
        self.gameover_time = self.GAMEOVER_TIME
        self.RUNNING_TIME = running_time
        self.running_time = self.RUNNING_TIME
        self.READY_TIME = ready_time
        self.ready_time = self.READY_TIME
        self.status = Status.READY
        self.time = 0.

    def running_step(self, dt):
        raise NotImplementedError

    def gameover(self):
        raise NotImplementedError

    def ready(self):
        raise NotImplementedError

    def running(self):
        raise NotImplementedError

    def run_steps(self, dt):
        self.time -= dt
        next_step = self.time <= 0.
        if not next_step:
            return
        if self.status == Status.RUNNING:
            self.status = Status.GAMEOVER
            self.time = self.GAMEOVER_TIME
            self.gameover()
        elif self.status == Status.GAMEOVER:
            self.status = Status.READY
            self.time = self.READY_TIME
            self.ready()
        elif self.status == Status.READY:
            self.status = Status.RUNNING
            self.time = self.RUNNING_TIME
            self.running()
        if self.status == Status.RUNNING:
            self.running_step(dt)

class Standard(AbstractGameMode):
    def __init__(self, server, engine, powerup=5):
        super().__init__(server, engine)
        self.powerup = powerup
        self.spawn_each = powerup/self.RUNNING_TIME
        self.spawn_time = self.spawn_each

    def running_step(self, dt):
        self.spawn_time -= dt

    def ready(self):
        pass
    
    def running(self):
        pass

    def gameover(self):
        pass
