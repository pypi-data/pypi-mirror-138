# -*- coding: utf-8 -*-
from luma.menu.widgets import Widget


class Scrollbar(Widget):
    """
    x,y is the point of the arrow
    arrows are 5x3 / 3x5
    """
    
    # @todo eventually display a line for % of scrolled content?
    # @todo also remove the arrow in the direction that there isn't more content to scroll
    def __init__(self, view, orient="vertical", command=""):
        super().__init__(view)
        self._orient = orient
        self._up = False
        self._down = False
        self._left = False
        self._right = False
        self._width = self.view.ctrl.display.device.width
        self._height = self.view.ctrl.display.device.height
        self._titlesize = 12  # added a 2px margin (should it be in render or up_arrow)
    
    @staticmethod
    def up_arrow(x1, y1):
        return [(x1,y1), (x1-2,y1+2), (x1+2,y1+2)]
    
    @staticmethod
    def down_arrow(x1, y1):
        return [(x1,y1), (x1+2,y1-2), (x1-2,y1-2)]
    
    @staticmethod
    def left_arrow(x1, y1):
        return [(x1,y1), (x1+2,y1+2), (x1+2,y1-2)]
    
    @staticmethod
    def right_arrow(x1, y1):
        return [(x1,y1), (x1-2,y1+2), (x1-2,y1-2)]
    
    def show_up(self, show=True):
        self._up = show
    
    def show_down(self, show=True):
        self._down = show
    
    def show_left(self, show=True):
        self._left = show
    
    def show_right(self, show=True):
        self._right = show
    
    def render(self, draw, *unused):
        # @todo any way of caching this, lots of repetitive maths
        #if self._orient == "vertical":
        #elif self._orient == "horizontal":
        if self._up:
            draw.polygon(self.up_arrow(self._width-3,self._titlesize), fill="white")
        if self._down:
            draw.polygon(self.down_arrow(self._width-3,self._height-5), fill="white")
        if self._left:
            draw.polygon(self.left_arrow(2,self._height-3), fill="white")
        if self._right:
            draw.polygon(self.right_arrow(self._width-5,self._height-3), fill="white")