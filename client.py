import pyglet
from pyglet.window import key
from polytanks.ogf4py.director import Director
from polytanks.ogf4py.scene import Scene
from polytanks.ogf4py_toyblock3 import component, system, toyblock3
from polytanks import assets

WIDTH = 640
HEIGHT = 360
UNIT = 16.

class KeyControl:
    def __init__(self):
        self.left_keys = (key.A, key.LEFT)
        self.right_keys = (key.D, key.RIGHT) 
        self.move = 0.

class InputSystem(toyblock3.System):
    def _update(self, entity):
        entity.body.vel_x = entity.input.move*UNIT*2.

class SpritesSystem(toyblock3.System):
    def _update(self, entity):
        body = entity.body
        sprite = entity.sprite
        sprite.x = body.x
        sprite.y = body.y

class Player:
    Input = KeyControl
    Body = component.Body
    Sprite = pyglet.sprite.Sprite
    def __init__(self, image, batch, groups):
        self.input = self.Input() 
        self.sprite = self.Sprite(image, batch=batch, group=groups[0])
        self.body = component.Body()

class Screen(Scene):
    def __init__(self):
        super().__init__(1)
        self.player = Player(assets.images["tank-base"], self.batch, self.groups)
        self.input_system = InputSystem()
        self.physics = system.PhysicsSystem(1./60., 0.)
        self.sprites_system = SpritesSystem()
        self.input_system.add_entity(self.player)
        self.physics.add_entity(self.player)
        self.sprites_system.add_entity(self.player)

    def init(self):
        pass

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

director = Director(width=WIDTH, height=HEIGHT)
director.scene = Screen()
pyglet.app.run()
