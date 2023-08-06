# -*- coding: utf-8 -*-


class Widget:
    # @todo should there we be able to declare a widget "static", so we don't waste time redrawing it? say the title.. and manually force redraw on lock/unlock  framebuffer diff?
    def __init__(self, view):
        self.view = view
        self._hidden = False

    @property
    def hidden(self):
        return self._hidden

    def hide(self):
        self._hidden = True
    
    def show(self):
        self._hidden = False
    
    def render(self, *unused):
        """
        This should be overriden, and prob better documented/implemented?
        """
        pass