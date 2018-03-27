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
from polytanks.event import event_manager
from polytanks import powerup
from polytanks.constants import UNIT

class Status:
    RUNNING = 0
    GAMEOVER = 1
    READY = 2

class AbstractGameMode:
    def __init__(self, server, engine, ready_time=5, running_time=10, gameover_time=3):
        self.server = server
        self.engine = engine
        self.gameover_time = gameover_time
        self.running_time = running_time
        self.ready_time = ready_time
        self.status = Status.READY
        self.time = self.ready_time

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
        if self.status == Status.RUNNING:
            self.running_step(dt)
        if not next_step:
            return
        if self.status == Status.RUNNING:
            self.status = Status.GAMEOVER
            self.time = self.gameover_time
            self.gameover()
        elif self.status == Status.GAMEOVER:
            self.status = Status.READY
            self.time = self.ready_time
            self.ready()
        elif self.status == Status.READY:
            self.status = Status.RUNNING
            self.time = self.running_time
            self.running()

    @property
    def is_ready(self):
        return self.status == Status.READY

    @property
    def is_running(self):
        return self.status == Status.RUNNING

    @property
    def is_gameover(self):
        return self.status == Status.GAMEOVER

class Standard(AbstractGameMode):
    def __init__(self, server, engine, powerup=5):
        super().__init__(server, engine)
        self.spawn_each = self.running_time/powerup
        self.spawn_time = self.spawn_each

    def running_step(self, dt):
        self.spawn_time -= dt
        if self.spawn_time <= 0:
            self.spawn_time = self.spawn_each
            effect = random.choice(powerup.effects)
            effect_i = powerup.effects.index(effect)
            player = self.engine.players[1]
            if not player:
                return
            x = player.body.x
            y = player.body.y + UNIT*3
            self.engine.add_powerup(x, y, effect) 
            event_manager.add_powerup_event()
            # TODO: obtener i del efecto
            # TODO: posicion de (un) jugador
            # TODO: asignar x e y al powerup a partir del jugador
            print("add powerup!")

    def ready(self):
        pass
    
    def running(self):
        pass

    def gameover(self):
        pass
