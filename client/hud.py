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

import pyglet
from pyglet import clock
from polytanks.constants import WIDTH, HEIGHT, UNIT

class Clock:
    def __init__(self, batch, group):
        self.seconds = 0.
        self.total_seconds = 0.
        self.label = pyglet.text.Label("",
            batch=batch,
            group=group)

    def set(self, total_seconds):
        self.total_seconds = total_seconds
        self.seconds = total_seconds
        self.update_text()

    def start(self):
        clock.schedule(self.update)

    def stop(self):
        clock.unschedule(self.update)

    def update_text(self):
        seconds = self.seconds % 60
        minutes = self.seconds // 60
        self.label.text = "{} : {}".format(minutes, seconds)

    def update(self, dt):
        self.seconds += -dt
        if self.seconds < 0.:
            self.seconds = 0.
        self.update_text()

class HUD:
    MESSAGE = "READY"
    def __init__(self, batch, groups):
        self.message = pyglet.text.Label(self.MESSAGE,
            x=WIDTH/2., y=HEIGHT/2.,
            anchor_x="center", anchor_y="center",
            batch=batch, group=groups[4])
        self.clock = Clock(batch, groups[4])
        self.clock.label.y = HEIGHT-32. 
        self.hide_message()
        self.results = pyglet.text.Label(
            "Hola mundo\nGuay\n\nJeje",
            anchor_x="center", anchor_y="center",
            batch=batch, group=groups[4],
            multiline=True, width=WIDTH/4.
        )

    def show_message(self):
        self.message.color = self.message.color[:3] + (255,)

    def hide_message(self):
        self.message.color = self.message.color[:3] + (0,)

    def show_clock(self, seconds):
        self.clock.label.y = HEIGHT-32.
        self.clock.set(seconds) 
        self.clock.start()

    def hide_clock(self):
        self.clock.label.y = HEIGHT+32. 
        self.clock.stop()

    def show_results(self):
        self.results.x = WIDTH/2.
        self.results.y = HEIGHT/2.

    def hide_results(self):
        self.results.x = WIDTH*2.
