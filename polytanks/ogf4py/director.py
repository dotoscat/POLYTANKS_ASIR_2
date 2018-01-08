# ogf4py
# Copyright (C) 2017  Oscar Triano @cat_dotoscat

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
import pyglet
from pyglet.window import key
from pyglet.gl import glViewport, glOrtho, glMatrixMode, glLoadIdentity
from pyglet import gl

class Director(pyglet.window.Window):
    """A director manages scenes and have convenients methods such manipulate
    color background of the window or make screenshots.
    
    Parameters:
        vwidth (int or float): Virtual width.
        vheight (int or float): Virtual height.
        
    Returns:
        An instance of Director.
    """
    _director = None
    _scenes = {}

    @staticmethod
    def add_scene(key, scene):
        """Add an scene assigned to a key."""
        Director._scenes[key] = scene

    @staticmethod
    def set_scene(key):
        """Set the current scene by its key."""
        if Director._director is None: return
        Director._director.scene = Director._scenes[key]

    @classmethod
    def get_scene(cls, key):
        """Get a scene stored but its key."""
        return cls._scenes[key]

    def __init__(self, *args, vwidth=None, vheight=None,
    exit_with_ESC=True, **kwargs):
        super(Director, self).__init__(*args, **kwargs)
        self._vwidth = vwidth
        self._vheight = vheight
        self._scene = None
        self._exit_with_ESC = exit_with_ESC
        Director._director = self

    def set_background_color(self, r, g, b):
        gl.glClearColor(r, g, b, 1.)

    @property
    def scene(self):
        """Set the current scene here."""
        return self._scene

    @scene.setter
    def scene(self, scene):
        if self._scene is not None:
            self.remove_handlers(self._scene)
            self._scene.quit()
            self._scene.director = None
            pyglet.clock.unschedule(self._scene.update)
        self._scene = scene
        self.push_handlers(scene)
        pyglet.clock.schedule(scene.update)
        scene.director = self
        scene.init()

    def get_virtual_xy(self, x, y):
        vx = x if self._vwidth is None else x/self.width*self._vwidth
        vy = y if self._vheight is None else y/self.height*self._vheight
        return vx, vy

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE and self._exit_with_ESC:
            super(Director, self).on_key_press(symbol, modifiers)
        elif symbol != key.ESCAPE:
            super(Director, self).on_key_press(symbol, modifiers)
        if symbol == key.F4:
            self.do_screenshot()

    def on_draw(self):
        self.clear()
        if self._scene is not None:
            self._scene.draw()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(gl.GL_PROJECTION)
        glLoadIdentity()
        width = self._vwidth if self._vwidth is not None else width
        height = self._vheight if self._vheight is not None else height
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(gl.GL_MODELVIEW)

    def do_screenshot(self):
        """Make a screenshot from current contents of the window."""
        now = datetime.now()# + str(now).replace(' ', '_')
        filename = 'screenshot' + '.png'
        pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
