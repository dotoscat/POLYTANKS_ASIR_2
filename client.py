import pyglet
from polytanks.ogf4py.director import Director
from polytanks.ogf4py.scene import Scene
from polytanks import assets

class Screen(Scene):
    def __init__(self):
        super().__init__(1)
        self.sprite = pyglet.sprite.Sprite(assets.images["tank-base"], batch=self.batch)

    def init(self):
        pass

    def quit(self):
        pass

    def update(self, dt):
        print("dt", dt)

director = Director()
director.scene = Screen()
pyglet.app.run()
