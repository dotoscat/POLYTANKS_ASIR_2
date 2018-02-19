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

from collections import deque
from weakref import proxy
import pyglet

class Scene(object):
    """Use scenes to organize what is going to happen on screen.
    
    An scene has at least a batch and *n* ordered groups used as layers.
        
    Parameters:
        n_groups (int): Number of groups (layers) for this scene.
        
    Returns:
        An instance of Scene.
    """

    def __init__(self, n_groups):
        self._director = None
        self._batch = pyglet.graphics.Batch()
        self._groups = [pyglet.graphics.OrderedGroup(i) for i in range(n_groups)]
        self._child = deque()
        self._focus = None

    @property
    def children(self):
        return self._child

    @property
    def director(self):
        """Is it just a proxy of :class:`Director`."""
        return self._director
        
    @director.setter
    def director(self, director):
        self._director = None if director is None else proxy(director)

    @property
    def batch(self):
        """Access to the scene batch."""
        return self._batch

    @property
    def groups(self):
        """Access to the ordered groups of this scene.
        
        Returns:
            A list of ordered groups.
        """
        return self._groups

    def draw(self):
        """Called by :class:`Director` to draw the graphics added to this scene.
        """
        self._batch.draw()

    def init(self):
        """This is called when this scene is set to the director.
        
        Does nothing, so you can override this to do something useful.
        """
        raise NotImplementedError("Implement an init for this scene.")

    def quit(self):
        """This is called when this scene is about to set another scene and *before* that scene.
        
        Does nothing, so you can override this to do something useful.
        """
        raise NotImplementedError("Implement a quite method when this scene is replaced.")

    def update(self, dt):
        """The scene's heart. This is called periodically.
        
        Does nothing, so you can override this to do something useful.
        
        Parameters:
            dt (float): Time elapsed from the last call to update.
        """
        raise NotImplementedError("Implement a update method for this scene.")

    def on_text(self, text):
        if self._focus:
            self._focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self._focus:
            self._focus.caret.on_text_motion(motion)

    def on_mouse_motion(self, x, y, dx, dy):
        get_virtual_xy = self.director.get_virtual_xy
        vx, vy = get_virtual_xy(x, y)
        vdx, vdy = get_virtual_xy(dx, dy)
        for child in self._child:
            child.on_mouse_motion(vx, vy, vdx, vdy)
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        vx, vy = self.director.get_virtual_xy(x, y)
        for child in self._child:
            if not child.visible: continue
            hit_test = getattr(child, "hit_test", None)
            if hit_test is None: continue
            text_entry = hit_test(vx, vy)
            if text_entry is None: continue
            if self._focus is not None:
                self._focus.caret.visible = False
                self._focus.caret.mark = 0
                self._focus.caret.position = 0
            self._focus = text_entry
            self._focus.caret.mark = 0
            self._focus.caret.position = len(text_entry.value)
            return
        if self._focus is not None:
            self._focus.caret.visible = False
            self._focus.caret.mark = 0
            self._focus.caret.position = 0
            self._focus = None
            
    def on_mouse_release(self, x, y, button, modifiers):
        vx, vy = self.director.get_virtual_xy(x, y)
        for child in self._child:
            child.on_mouse_release(vx, vy, button, modifiers)
