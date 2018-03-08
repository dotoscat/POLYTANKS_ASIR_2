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

class Control:
    def __init__(self):
        self.move = 0.
        self.pointer_x = 0.
        self.pointer_y = 0.
        self.touch_floor = False
        self.jumps = False
        self.jump_pressed = False

class Info:
    def __init__(self):
        self.touched_floor = False
