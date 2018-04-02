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

from polytanks.constants import WIDTH, HEIGHT, UNIT
import pyglet

class HUD:
    MESSAGE = "READY"
    def __init__(self, batch, groups):
        self.message = pyglet.text.Label(self.MESSAGE,
                                        x=WIDTH/2., y=HEIGHT/2.,
                                        anchor_x="center",
                                        anchor_y="center",
                                        batch=batch, group=groups[4])
        self.hide_message()

    def show_message(self):
        self.message.color = self.message.color[:3] + (255,)

    def hide_message(self):
        self.message.color = self.message.color[:3] + (0,)
