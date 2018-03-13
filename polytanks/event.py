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

from collections import deque
import struct
from toyblock3 import Pool

player_event_struct = struct.Struct("!BB")
player_make_struct = struct.Struct("!BBH")
player_make_value_struct = struct.Struct("!BBf")

PLAYER_JUMPS = 1
PLAYER_FLOATS = 2
PLAYER_TOUCHES_FLOOR = 3
PLAYER_NOCKED_OUT = 4
PLAYER_SHOOTS = 5
PLAYER_CANNON_MOVES = 6

PLAYER_MAKE_GROUP = (
    PLAYER_JUMPS,
    PLAYER_FLOATS,
    PLAYER_TOUCHES_FLOOR,
    PLAYER_NOCKED_OUT,
)

class Event:
    def __init__(self):
        self.id = 0
    
    def from_bytes(self, bytes):
        raise NotImplementedError

    def __bytes__(self):
        raise NotImplementedError

    def reset(self):
        self.id = 0

class _PlayerEvent(Event):
    def __init__(self):
        super().__init__()
        self.player_id = 0

    def from_bytes(self, bytes):
        self.id, self.player_id = player_event_struct.unpack(bytes)

    def __bytes__(self):
        return player_event_struct.pack(self.id, self.player_id)

    def reset(self):
        super().reset()
        self.player_id = 0

PlayerEvent = Pool(_PlayerEvent, 64)

class _PlayerMakeEvent(_PlayerEvent):
    def __init__(self):
        super().__init__()
        self.what_id = 0

    def from_bytes(self, bytes):
        self.id, self.player_id, self.what_id = player_make_struct.unpack(bytes)

    def __bytes__(self):
        return player_make_struct.pack(self.id, self.player_id, self.what_id)

    def reset(self):
        super().reset()

PlayerMakeEvent = Pool(_PlayerMakeEvent, 64)

class _PlayerMakeValueEvent(_PlayerEvent):
    def __init__(self):
        super().__init__()
        self.value = 0.

    def from_bytes(self, bytes):
        self.id, self.player_id, self.value = player_make_value_struct.unpack(bytes)

    def __bytes__(self):
        return player_make_value_struct.pack(self.id, self.player_id, self.value)

    def reset(self):
        super().reset()

PlayerMakeValueEvent = Pool(_PlayerMakeValueEvent, 64)

class EventManager:
    def __init__(self):
        self.events = deque()
        self._consumed = deque()

    def add_player_event(self, what, who):
        event = PlayerEvent()
        event.id = what
        event.player_id = who
        self.events.append(event)

    def add_player_make_event(self, what, who, what_object):
       event = PlayerMakeEvent()
       event.id = what
       event.player_id = who
       event.what_id = what_object 
       self.events.append(event)

    def from_bytes(self, data):
        total = len(data)
        offset = 0
        while offset < total:
            what = int.from_bytes(data[offset:offset+1], "big")
            if what == PLAYER_SHOOTS:
                what, who, what_object = player_make_struct.unpack_from(data, offset)
                self.add_player_make_event(what, who, what_object)
                offset += player_make_struct.size
            elif what in PLAYER_MAKE_GROUP:
                what, who = player_event_struct.unpack_from(data, offset)
                self.add_player_event(what, who)
                offset += player_event_struct.size
            elif what == PLAYER_CANNON_MOVES:
                what, who, value = player_make_value_struct.unpack_from(data, offset)
                offset += player_make_value_struct.size
            else:
                raise RuntimeError("Check event from bytes")

    def to_network(self):
        if not self.events:
            return
        # n_events = int.to_bytes(len(self.events), 1, "big")
        data = bytearray()
        # data += n_events
        events = self.events
        while events:
            event = events.pop()
            data += bytes(event)
            event.free()
        return data

    def clear(self):
        while self.events:
            self.events.pop().free()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.events:
            while self._consumed:
                self._consumed.pop().free()
            raise StopIteration
        event = self.events.pop()
        self._consumed.append(event)
        return event

event_manager = EventManager()
