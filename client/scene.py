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

from math import sin, cos, degrees
import toyblock3
import pyglet
from pyglet.window import key
from polytanks import level, protocol, snapshot, event
from polytanks.event import event_manager
from polytanks.constants import CANNON_JOINT, CANNON_LENGTH, BULLET_SPEED, WIDTH
from ogf4py.scene import Scene
from ogf4py.director import Director
from . import assets
from .engine import Engine

class Screen(Scene):
    INPUT_PER_SEC = 1./20.
    def __init__(self, client):
        super().__init__(4)
        self.client = client
        self.engine = Engine(self.batch, self.groups)
        self.player = None
        self.players_damage = {}
        # level.load_level(level.basic, self.pools["platform"])

    def init(self):
        self.director.set_mouse_cursor(assets.cursor)
        self.load()
        pyglet.clock.schedule_interval(self.send_input_to_server, self.INPUT_PER_SEC)
        # pyglet.clock.schedule_interval(self.request_full_snapshot, 1.)

    def load(self):
        self.engine.load_level()
        self.player = self.engine.add_player(self.client.id)[1]
        self.set_hud()

    def set_hud(self):
        n_players = self.client.n_players
        labels = {i: pyglet.text.Label("{} player".format(i), batch=self.batch, group=self.groups[3])
                for i in range(1,n_players+1)}
        self.players_damage = labels
        #if n_players == 2:
            

    def quit(self):
        self.director.set_mouse_cursor(None)
        pyglet.clock.unschedule(self.send_input_to_server)
        pyglet.clock.unschedule(self.request_full_snapshot)
        self.engine.remove_player(self.client.id)

    def request_full_snapshot(self, dt):
        self.client.server_send(protocol.request_snapshot_struct.pack(protocol.REQUEST_SNAPSHOT, self.client.id))

    def update(self, dt):
        self.client.step()
        self.engine.update(dt)

    def send_input_to_server(self, dt):
        input = self.player.input
        input_data = (
            protocol.command_id_struct.pack(protocol.INPUT, self.client.id)
            + bytes(input)
        )
        self.client.game_send(input_data)
        # print("send input to server", dt) 

    def udp_from_server(self, socket):
        data = socket.recv(1024)
        command = protocol.command(data)
        if command == protocol.SNAPSHOT:
            # print("snapshot payload", data)
            snapshot_data = data[1:]
            response = protocol.snapshotack_struct.pack(protocol.SNAPSHOT_ACK, self.client.id)
            socket.send(response)
            self.apply_snapshot_data(snapshot_data)
            # print("udp message from server", data)
    
    def rudp_from_server(self, message, address, mailbox):
        command = protocol.command(message)
        if command == protocol.EVENT:
            event_data = message[1:]
            self.manage_events(event_data)
        # print("received '{}' from {}".format(message, address))

    def tcp_from_server(self, data):
        command = protocol.command(data)
        if command == protocol.SNAPSHOT:
            snapshot_data = data[1:]
            self.apply_snapshot_data(snapshot_data)
        elif command == protocol.EVENT:
            self.manage_events(data[1:])

    def manage_events(self, data):
        event_manager.from_bytes(data)
        for eve in event_manager:
            if eve.id == event.PLAYER_TOUCHES_FLOOR:
                print("player {} touches the floor".format(eve.player_id))
            elif eve.id == event.PLAYER_JUMPS:
                print("player {} jumps".format(eve.player_id))
            elif eve.id == event.PLAYER_FLOATS:
                print("player {} floats".format(eve.player_id))
            elif eve.id == event.PLAYER_SHOOTS:
                print("player {} shoots {}".format(eve.owner, eve.bullet_id))
                # TODO: Tratar evento de player_shoots
                id, bullet = self.engine.add_bullet(
                    eve.owner,
                    eve.x,
                    eve.y,
                    eve.angle,
                    eve.power,
                    id=eve.bullet_id)

    def apply_snapshot_data(self, data):
        tsnapshot = snapshot.Snapshot()
        tsnapshot.from_diff_data(data)
        tsnapshot.apply_to_engine(self.engine)
        tsnapshot.free()
        # print("client receives", data)

    def _disconnected(self):
        Director.set_scene("main")

    def on_key_press(self, symbol, modifiers):
        if symbol in self.player.input.left_keys:
            self.player.input.move = -1.
        if symbol in self.player.input.right_keys:
            self.player.input.move = 1.
        if symbol in self.player.input.jump_keys:
            self.player.input.jumps = True
        if symbol == key.L:
            self.client.disconnect_from_server(self._disconnected)

    def on_key_release(self, symbol, modifiers):
        if symbol in self.player.input.left_keys:
            self.player.input.move = 0.
        if symbol in self.player.input.right_keys:
            self.player.input.move = 0.
        if symbol in self.player.input.jump_keys:
            self.player.input.jumps = False

    def _update_pointer(self, x, y):
        self.player.input.pointer_x = x
        self.player.input.pointer_y = y

    def on_mouse_motion(self, x, y, dx, dy):
        self._update_pointer(x, y)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self._update_pointer(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        print("charge shot", self.player.input.shoots)
        self.player.input.shoots = True

    def on_mouse_release(self, x, y, button, modifiers):
        print("unrelease shot", self.player.input.shoots)
        self.player.input.shoots = False

class Main(Scene):
    def __init__(self, client, address):
        super().__init__(1)
        self.client = client
        self.address = address

    def init(self):
        pass

    def quit(self):
        pass

    def update(self, dt):
        self.client.step() 

    def on_key_press(self, symbol, modifiers):
        if symbol == key.C:
            game_scene = Director.get_scene("game")
            self.client.connect_to_server(
                self.address, game_scene.udp_from_server,
                game_scene.tcp_from_server, self._connected, game_scene.rudp_from_server
            )

    def _connected(self):
        Director.set_scene("game")
