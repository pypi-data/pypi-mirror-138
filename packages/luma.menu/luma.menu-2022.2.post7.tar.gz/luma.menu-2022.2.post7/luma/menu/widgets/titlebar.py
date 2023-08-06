# -*- coding: utf-8 -*-
from luma.menu.widgets import Widget


class Titlebar(Widget):
    def __init__(self, view, text):
        super().__init__(view)
        self._text = text
        self._width = self.view.ctrl.display.device.width
        self._highlighted = False
    
    @property
    def highlighted(self):
        return self._highlighted
    
    def highlight(self, highlight=True):
        self._highlighted = highlight
        self.view.force_redraw()
    
    def render(self, draw, *unused):
        text_width = draw.textsize(self._text, self.view.font)[0]  # adjust for kerning (1 per letter it seems)
        text_height = draw.textsize(self._text, self.view.font)[1] + 1  # 1px extra makes bottom/top have 2px padding
        x = ((self._width - text_width) / 2)  # horizontal center the text
        if self._highlighted:
            draw.rectangle((0, 0, self._width, text_height), fill="white")  # white rectangle titlebar
            draw.text((x, 0), self._text, font=self.view.font, fill="black")  # do not fill pixels (black on white)
        else:
            draw.line((0, text_height, self._width, text_height), fill="white")  # white line separator at the bottom
            draw.text((x, 0), self._text, font=self.view.font, fill="white")