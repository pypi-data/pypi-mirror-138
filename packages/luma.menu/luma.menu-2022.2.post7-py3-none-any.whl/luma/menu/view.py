# -*- coding: utf-8 -*-
from luma.core.render import canvas
from PIL import ImageFont
from pathlib import Path
import time

"""
@idea if all views will have a title, that follows submenus, then create a TitledWidget of sorts to remove .lock/.unlock from GPSView, etc..
@idea create a lock/unlock event for controllers to respond to and do actions/change their title if needed?
"""


class View:
    def __init__(self, ctrl):
        self.ctrl = ctrl
        # @todo move these somewhere else, improve this, fonts should be elsewhere and passed or set?
        file_path = Path(__file__)
        self.font = ImageFont.truetype(str(file_path.parent / "fonts/DejaVuSansMono.ttf"), 9, encoding="unic")  # 5x7 pixel font
        self.font_alt = ImageFont.truetype(str(file_path.parent / "fonts/liberation-mono.regular.ttf"), 9, encoding="unic")
        self.interval = 10  # default redraw every 10 seconds
        self._last_updated = 0
        self._previous_menu = None
        self.layout = list()
        self.create_widgets()

    def create_widgets(self):
        """
        This should be overriden, and prob better documented/implemented?
        """
        pass
    
    def should_redraw(self):
        return time.time() - self._last_updated > self.interval
    
    def force_redraw(self):
        self._last_updated = 0
        self.ctrl.draw_view()
    
    def update(self, *args, **kwargs):
        with canvas(self.ctrl.display.device) as draw:
            for widget in self.layout:
                if not widget.hidden:
                    widget.render(draw, *args, **kwargs)
        self._last_updated = time.time()

    def show_menu(self, menu):
        """
        Shows a passed menu, supports the cascading menu feature
        """
        # @todo add validation of sorts?
        self._previous_menu = self.menu
        self._previous_menu.hide()
        self.menu = menu
        self.menu.show()
        #self.title.text = self.menu.title  # @todo check why this isnt working
        self.force_redraw()
    
    def show_previous_menu(self):
        """
        Returns to previous menu, supports the cascading menu feature
        """
        if not self._previous_menu:
            return
        self.menu.hide()
        self.menu = self._previous_menu
        self.menu.show()
        #self.title.text = self.menu.title  # @todo check why this isnt working
        self.force_redraw()
    
    def popover(self, text):
        """
        Draw a small rectangular box with a short message that can be dismissed
        Useful for error messages?
        limit characters? wrap long sentences?
        """
        raise NotImplementedError
    
    def lock(self):
        """
        This should be overriden, and prob better documented/implemented?
        """
        self.title.text = "LOCKED"
    
    def unlock(self):
        """
        This should be overriden, and prob better documented/implemented?
        """
        self.title.text = self._title