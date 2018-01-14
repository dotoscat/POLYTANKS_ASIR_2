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

class TankGraphic:
    def __init__(self, batch, groups, group_start):
       self.base = pyglet.sprite.Sprite(assets.images["tank-base"], batch=batch, group=groups[group_start])
       self.cannon = pyglet.sprite.Sprite(assets.images["tank-cannon"], batch=batch, group=groups[group_start - 1])
       self.cannon_offset = (0., 0.)
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
        self.cannon.y = self.base.y + self.cannon_offset[0]

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
    Sprite = TankGraphic
    def __init__(self, batch, groups):
        self.input = self.Input() 
        self.sprite = self.Sprite(batch, groups, 1)
        self.body = component.Body()

class Screen(Scene):
    def __init__(self):
        super().__init__(3)
        self.player = Player(self.batch, self.groups)
        self.input_system = InputSystem()
        self.physics = system.PhysicsSystem(1./60.)
        self.sprites_system = SpritesSystem()
        self.input_system.add_entity(self.player)
        self.physics.add_entity(self.player)
        self.sprites_system.add_entity(self.player)

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

director = Director(width=WIDTH, height=HEIGHT)
director.scene = Screen()
pyglet.app.run()
