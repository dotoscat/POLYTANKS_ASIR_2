import pyglet
from polytanks.ogf4py.director import Director
from polytanks.ogf4py.scene import Scene
from polytanks.ogf4py_toyblock3 import component, system
from polytanks import assets

WIDTH = 640
HEIGHT = 360

class Player:
    Body = component.Body
    Sprite = pyglet.sprite.Sprite
    def __init__(self, image, batch, groups):
        self.sprite = self.Sprite(image, batch=batch, group=groups[0])
        self.body = component.Body()

class Screen(Scene):
    def __init__(self):
        super().__init__(1)
        self.player = Player(assets.images["tank-base"], self.batch, self.groups)

    def init(self):
        pass

    def quit(self):
        pass

    def update(self, dt):
        print("dt", dt)

    def key_down(self, symbol, modifiers):
        pass

director = Director(width=WIDTH, height=HEIGHT)
director.scene = Screen()
pyglet.app.run()
