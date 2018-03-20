#/usr/bin/env python
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

import os
import sys
sys.path.insert(0, os.path.abspath(__package__))
import pyglet
from ogf4py.director import Director
from polytanks.constants import WIDTH, HEIGHT
from client.client import Client
from client.scene import Screen, Main

if __name__ == "__main__":
    ADDRESS = ("127.0.0.1", 1337)
    client = Client()
    director = Director(width=WIDTH, height=HEIGHT)
    Director.add_scene("main", Main(client, ADDRESS))
    Director.add_scene("game", Screen(client))
    Director.set_scene("main")
    pyglet.app.run()
