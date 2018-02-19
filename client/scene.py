import toyblock3
from polytanks import level, assets
from ogf4py.scene import Scene

class Screen(Scene):
    def __init__(self):
        super().__init__(3)
        self.pools = {
            "player": toyblock3.Manager(Player, 4, self.batch, self.groups),
            "platform": toyblock3.Pool(Platform, 64, self.batch, self.groups[0])
        }
        self.player = Player(self.batch, self.groups)
        self.player = self.pools["player"]()
        self.player.body.x = 64.
        self.player.body.y = 64.
        self.input_system = input_system
        self.physics = physics_system
        self.sprites_system = sprites_system
        level.load_level(level.basic, self.pools["platform"])

    def init(self):
        self.director.set_mouse_cursor(assets.cursor)

    def quit(self):
        pass

    def update(self, dt):
        self.input_system()
        self.physics()
        self.sprites_system()

    def on_key_press(self, symbol, modifiers):
        if symbol in self.player.input.left_keys:
            self.player.input.move = -1.
        if symbol in self.player.input.right_keys:
            self.player.input.move = 1.

    def on_key_release(self, symbol, modifiers):
        if symbol in self.player.input.left_keys:
            self.player.input.move = 0.
        if symbol in self.player.input.right_keys:
            self.player.input.move = 0.

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.input.pointer_x = x
        self.player.input.pointer_y = y

class Main(Scene):
    def __init__(self, client):
        super().__init__(1)
        self.client = client

    def init(self):
        pass

    def quit(self):
        pass

    def update(self, dt):
        self.client.step() 

    def udp_from_server(self, socket):
        data = socket.recv(1024)
        command = protocol.command(data)
        if command == protocol.SNAPSHOT:
            response = protocol.snapshotack_struct.pack(protocol.SNAPSHOT_ACK, self.client.id)
            socket.send(response)
            print("udp message from server", data)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.C:
            self.client.connect_to_server(ADDRESS, self.udp_from_server)
        elif symbol == key.D:
            self.client.disconnect_from_server()
