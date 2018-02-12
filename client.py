import socket
import selectors
from math import atan2, degrees
import pyglet
from pyglet.window import key
import toyblock3
from polytanks.ogf4py.director import Director
from polytanks.ogf4py.scene import Scene
from polytanks.ogf4py_toyblock3 import component, system 
from polytanks import assets, level, protocol
from polytanks.constants import WIDTH, HEIGHT, UNIT

class KeyControl:
    def __init__(self):
        self.left_keys = (key.A, key.LEFT)
        self.right_keys = (key.D, key.RIGHT) 
        self.move = 0.
        self.pointer_x = 0.
        self.pointer_y = 0.

class TankGraphic:
    def __init__(self, batch, groups, group_start):
       self.base = pyglet.sprite.Sprite(assets.images["tank-base"], batch=batch, group=groups[group_start])
       self.cannon = pyglet.sprite.Sprite(assets.images["tank-cannon"], batch=batch, group=groups[group_start - 1])
       self.cannon_offset = (0., 4.)
       self._update()

    @property
    def x(self):
        return self.base.x

    @x.setter
    def x(self, value):
        self.base.x = value
        self._update()
        
    @property
    def y(self):
        return self.base.y

    @y.setter
    def y(self, value):
        self.base.y = value
        self._update()

    def _update(self):
        self.cannon.x = self.base.x + self.cannon_offset[0]
        self.cannon.y = self.base.y + self.cannon_offset[1]

    def update_cannon_angle(self, x, y):
        angle = atan2(y - self.cannon.y, x - self.cannon.x)
        self.cannon.rotation = degrees(-angle)

class InputSystem(toyblock3.System):
    def _update(self, entity):
        entity.body.vel_x = entity.input.move*UNIT*2.
        entity.sprite.update_cannon_angle(entity.input.pointer_x, entity.input.pointer_y)

input_system = InputSystem()

class SpritesSystem(toyblock3.System):
    def _update(self, entity):
        body = entity.body
        sprite = entity.sprite
        sprite.x = body.x
        sprite.y = body.y

sprites_system = SpritesSystem()
physics_system = system.PhysicsSystem(1./60.)

class Player:
    SYSTEMS = (input_system, physics_system, sprites_system)
    Input = KeyControl
    Body = component.Body
    Sprite = TankGraphic
    def __init__(self, batch, groups):
        self.input = self.Input() 
        self.sprite = self.Sprite(batch, groups, 1)
        self.body = component.Body()
    def reset(self):
        pass

class Platform:
    SYSTEMS = ()
    Sprite = pyglet.sprite.Sprite
    def __init__(self, batch, group):
        self.sprite = self.Sprite(assets.images["platform"], batch=batch, group=group)
    def reset(self):
        pass

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

class Client:
    def __init__(self):
        self.selectors = selectors.DefaultSelector()
        self.server_address = None
        self.id = 0
        self.server_connection = None
        self.game_connection = None

    def __del__(self):
        self.selectors.close()

    @property
    def connected(self):
        return self.id > 0

    def connect_to_server(self, address):
        if self.connected:
            return
        self.server_connection = socket.socket()
        self.server_connection.connect(address)
        self.server_connection.send(protocol.CONNECT.to_bytes(4, "big"))
        response = self.server_connection.recv(32)
        command = protocol.command(response)
        if command == protocol.CONNECTED:
            self.id = int.from_bytes(response[4:8], "big")
            self.server_address = address
            self.server_game = socket.socket(type=socket.SOCK_DGRAM)
            self.server_game.connect(address)
            self.server_game.setblocking(False)
        else:
            self.server_connection.close()

    def disconnect_from_server(self):
        if not self.connected:
            return
        self.server_connection.send(
            protocol.disconnect_struct.pack(protocol.DISCONNECT, self.id))
        response = self.server_connection.recv(32)
        print("response", response)
        if response == b"OK":
            self.id = 0
            self.server_address = None
            self.server_connection.close()
            self.game_connection.close()

class Main(Scene):
    def __init__(self, client):
        super().__init__(1)
        self.client = client

    def init(self):
        pass

    def quit(self):
        pass

    def update(self, dt):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.C:
            self.client.connect_to_server(ADDRESS)
        elif symbol == key.D:
            self.client.disconnect_from_server()

if __name__ == "__main__":
    ADDRESS = ("127.0.0.1", 1337)
    client = Client()
    #client.connect_to_server(ADDRESS)
    #print("connected", client.connected)
    #client.disconnect_from_server()
    director = Director(width=WIDTH, height=HEIGHT)
    director.scene = Main(client)
    pyglet.app.run()
