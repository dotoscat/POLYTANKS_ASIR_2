import toyblock3
import pyglet
from pyglet.window import key
from polytanks import level, protocol, snapshot
from ogf4py.scene import Scene
from ogf4py.director import Director
from . import assets
from .engine import Engine

class Screen(Scene):
    INPUT_PER_SEC = 1./20.
    def __init__(self, client):
        super().__init__(3)
        self.client = client
        self.engine = Engine(self.batch, self.groups)
        self.player = None
        # level.load_level(level.basic, self.pools["platform"])

    def init(self):
        self.director.set_mouse_cursor(assets.cursor)
        self.player = self.engine.add_player(self.client.id)[1]
        pyglet.clock.schedule_interval(self.send_input_to_server, self.INPUT_PER_SEC)
        # pyglet.clock.schedule_interval(self.request_full_snapshot, 1.)

    def quit(self):
        self.director.set_mouse_cursor(None)
        pyglet.clock.unschedule(self.send_input_to_server)
        self.engine.remove_player(self.client.id)

    def request_full_snapshot(self, dt):
        self.client.server_send(protocol.request_snapshot_struct.pack(protocol.REQUEST_SNAPSHOT, self.client.id))

    def update(self, dt):
        self.client.step()
        self.engine.update(dt)

    def send_input_to_server(self, dt):
        input = self.player.input
        data_input = protocol.input_struct.pack(protocol.INPUT, self.client.id,
            input.move)
        self.client.game_send(data_input)
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

    def tcp_from_server(self, data):
        command = protocol.command(data)
        if command == protocol.SNAPSHOT:
            snapshot_data = data[1:]
            print("requested snapshot_data", snapshot_data)
            self.apply_snapshot_data(snapshot_data)

    def apply_snapshot_data(self, data):
        tsnapshot = snapshot.Snapshot()
        tsnapshot.from_diff_data(data)
        tsnapshot.apply_to_engine(self.engine)
        tsnapshot.free()
        # print("client receives", data)


    def on_key_press(self, symbol, modifiers):
        if symbol in self.player.input.left_keys:
            self.player.input.move = -1.
        if symbol in self.player.input.right_keys:
            self.player.input.move = 1.
        if symbol == key.L and self.client.disconnect_from_server():
            Director.set_scene("main")

    def on_key_release(self, symbol, modifiers):
        if symbol in self.player.input.left_keys:
            self.player.input.move = 0.
        if symbol in self.player.input.right_keys:
            self.player.input.move = 0.

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.input.pointer_x = x
        self.player.input.pointer_y = y

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
            self.client.connect_to_server(self.address, game_scene.udp_from_server,
                game_scene.tcp_from_server, self._connected)

    def _connected(self):
        Director.set_scene("game")
