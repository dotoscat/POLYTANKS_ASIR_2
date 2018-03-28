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
player_shoots_struct = struct.Struct("!BBeeeHe?H")
player_hurt_struct = struct.Struct("!BBH")
add_powerup_struct = struct.Struct("!BeeB")
modify_player_struct = struct.Struct("!BBH")

PLAYER_JUMPS = 1
PLAYER_FLOATS = 2
PLAYER_TOUCHES_FLOOR = 3
PLAYER_NOCKED_OUT = 4
PLAYER_SHOOTS = 5
PLAYER_CANNON_MOVES = 6
PLAYER_HURT = 7
ADD_POWERUP = 8
MODIFY_HEALTH = 9

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
        pass

    def __bytes__(self):
        raise NotImplementedError

    def reset(self):
        self.id = 0

class _Modify(Event):
    def __init__(self):
        super().__init__()
        self.player_id = 0
        self.amount = 0

    def __bytes__(self):
        return modify_player_struct.pack(self.id, self.player_id, self.amount)

Modify = Pool(_Modify, 64)

class _AddPowerup(Event):
    def __init__(self):
        super().__init__()
        self.effect_i = 0
        self.x = 0.
        self.y = 0.

    def __bytes__(self):
        return add_powerup_struct.pack(self.id, self.x, self.y, self.effect_i)

    def from_bytes(self, buffer):
        self.id, self.x, self.y, self.effect_i = add_powerup_struct.unpack(buffer)

AddPowerup = Pool(_AddPowerup, 64)

class _PlayerHurt(Event):
    def __init__(self):
        super().__init__()
        self.player_id = 0
        self.damage = 0

    def __bytes__(self):
        return player_hurt_struct.pack(self.id, self.player_id, self.damage) 

    def from_bytes(self, bytes):
        self.id, self.player_id, self.damage = player_hurt_struct.unpack(bytes)

    def reset(self):
        super().reset()
        self.player_id = 0

PlayerHurt = Pool(_PlayerHurt, 64)

class _ShotEvent(Event):
    def __init__(self):
        super().__init__()
        self.owner = 0
        self.x = 0.
        self.y = 0.
        self.angle = 0.
        self.power = 0.
        self.bullet_id = 0.
        self.speed = 0.
        self.gravity = False

    def __bytes__(self):
        print("bytes", self.power, self.bullet_id, self.speed, self.gravity)
        return player_shoots_struct.pack(self.id, self.owner, self.x, self.y
        , self.angle, self.power, self.speed, self.gravity, self.bullet_id)

    def from_bytes(self, buffer):
        self.id, self.owner, self.x, self.y, self.angle, self.power, self.bullet_id, self.speed, self.gravity = player_shoots_struct.unpack(buffer)

    def reset(self):
        self.owner = 0
        self.x = 0.
        self.y = 0.
        self.angle = 0.
        self.power = 0.
        self.bullet_id = 0.

ShotEvent = Pool(_ShotEvent, 64)

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

    def add_heal_event(self, player_id, amount):
        self.add_modify_player(MODIFY_HEALTH, player_id, amount)

    def add_modify_player(self, what, player_id, amount):
        event = Modify()
        event.id = what
        event.player_id = player_id
        event.amount = amount

    def add_powerup_event(self, x, y, effect_i):
        event = AddPowerup()
        event.id = ADD_POWERUP
        event.effect_i = effect_i
        event.x = x
        event.y = y
        self.events.append(event)

    def add_player_event(self, what, who):
        event = PlayerEvent()
        event.id = what
        event.player_id = who
        self.events.append(event)

    def add_player_hurt(self, who, damage):
        event = PlayerHurt()
        event.id = PLAYER_HURT
        event.player_id = who
        event.damage = damage
        self.events.append(event)

    def add_player_make_event(self, what, who, what_object):
       event = PlayerMakeEvent()
       event.id = what
       event.player_id = who
       event.what_id = what_object 
       self.events.append(event)

    def add_shot_event(self, owner, x, y, angle, power, speed, gravity, bullet_id):
        event = ShotEvent()
        event.id = PLAYER_SHOOTS
        event.owner = owner
        event.x = x
        event.y = y
        event.angle = angle
        event.power = power
        event.bullet_id = bullet_id
        event.speed = speed
        event.gravity = gravity
        self.events.append(event)

    def from_bytes(self, data):
        total = len(data)
        offset = 0
        while offset < total:
            what = int.from_bytes(data[offset:offset+1], "big")
            if what == MODIFY_HEALTH:
                what, player_id, amount = modify_player_struct.unpack_from(data, offset)
                self.add_heal_event(player_id, amount)
                offset += modify_player_struct.size
            elif what == ADD_POWERUP:
                what, x, y, effect_i = add_powerup_struct.unpack_from(data, offset)
                self.add_powerup_event(x, y, effect_i)
                offset += add_powerup_struct.size
            elif what == PLAYER_HURT:
                what, player_id, damage = player_hurt_struct.unpack_from(data, offset)
                self.add_player_hurt(player_id, damage)
                offset += player_hurt_struct.size
            elif what == PLAYER_SHOOTS:
                what, owner, x, y, angle, power, speed, gravity, bullet_id = player_shoots_struct.unpack_from(data, offset)
                self.add_shot_event(owner, x, y, angle, power, speed, gravity, bullet_id)
                offset += player_shoots_struct.size
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
