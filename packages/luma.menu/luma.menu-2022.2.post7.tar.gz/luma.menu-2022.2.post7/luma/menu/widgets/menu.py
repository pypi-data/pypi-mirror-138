# -*- coding: utf-8 -*-
from luma.menu.widgets import Widget


class Menu(Widget):
    """
    Menu entries can be simple text, command/callback, casdading menu/submenu
    Widget is redrawn as a whole, no "hotspot" like luma viewport provides
    """
    
    def __init__(self, view, xy, title="", page=0):
        if len(xy) != 4:
            raise ValueError("xy argument has to be a 4-item tuple (x1,y1,x2,y2)")

        super().__init__(view)
        self._title = title
        self._xy = xy
        self._width = xy[2]-xy[0]
        self._height = xy[3]-xy[1]
        self._linesize = 10  # this should use draw.textsize("placeholder")[1]? or bbox? but without knowing the text?
        self._current_page = page
        self._current_highlight = 0
        self._highlightable_list = list()
        self._per_page = self._height//self._linesize  # integer division to only keep the whole number
        self._menu = list()
        self._menu_page = list()
    
    @property
    def title(self):
        return self._title
    
    @property
    def entries(self):
        return self._menu
    
    @property
    def highlightable(self):
        return True if self._highlightable_list else False

    def clear(self):
        self._menu = list()
    
    def page_up(self):
        if self._menu and not self._hidden:
            self._current_page -= 1
            if self._current_page < 0:
                self._current_page += 1
            else:
                # Redraw only on a new page
                self.view.force_redraw()

    def page_down(self):
        if self._menu and not self._hidden:
            count_ = (len(self._menu)-1) // self._per_page
            self._current_page += 1
            if self._current_page > count_:
                self._current_page -= 1
            else:
                # Redraw only on a new page
                self.view.force_redraw()
    
    def highlight_up(self):
        if self._highlightable_list and not self._hidden:
            count_ = len(self._highlightable_list)
            self._current_highlight -= 1
            if self._current_highlight < 0:
                self._current_highlight = count_-1
            
            self._current_page = self.find_entry_page(self.current_highlighted_entry())
            self.view.force_redraw()
    
    def highlight_down(self):
        if self._highlightable_list and not self._hidden:
            count_ = len(self._highlightable_list)
            self._current_highlight += 1
            if self._current_highlight >= count_:
                self._current_highlight = 0
            
            self._current_page = self.find_entry_page(self.current_highlighted_entry())
            self.view.force_redraw()
    
    def current_highlighted_entry(self):
        return self._highlightable_list[self._current_highlight]
    
    def find_entry_page(self, widget):
        pages_count = len(self._menu) // self._per_page
        
        for page_num in range(pages_count+1):
            start = self._per_page * page_num
            end = start + self._per_page
            menu_page = self._menu[start:end]
            if widget in menu_page:
                return page_num
        
        raise ValueError("Failed to find widget in menu")
    
    def render(self, draw, *args, **kwargs):
        # Do not render if this isn't the currently displayed menu
        if self._hidden:
            return
        
        # @todo is there a smarter way to do this?
        if self._highlightable_list:
            highlighted_entry = self._highlightable_list[self._current_highlight]
        else:
            highlighted_entry = None  # should never match widget below
        
        start = self._per_page * self._current_page
        end = start + self._per_page
        self._menu_page = self._menu[start:end]
        for i, entry in enumerate(self._menu_page):
            x = self._xy[0]  # obviously stays the same, only y should change
            y = self._xy[1]+(self._linesize*i)
            xy = (x, y)
            if self.view.ctrl.is_interactive and entry is highlighted_entry:
                entry.highlight()
            else:
                # Remove highlight if previously applied
                entry.highlight(False)
            entry.render(draw, xy, *args, **kwargs)
        
        # Draw scroll arrows
        if start > 0:
            self.view.scrollbar.show_up()
        else:
            self.view.scrollbar.show_up(False)
        if end < len(self._menu):
            self.view.scrollbar.show_down()
        else:
            self.view.scrollbar.show_down(False)
    
    def add_text(self, text):
        entry = MenuText(self, text)
        self._menu.append(entry)
    
    def add_command(self, text, command):
        entry = MenuCommand(self, text, command)
        self._menu.append(entry)
        self._highlightable_list.append(entry)


class MenuText:
    """
    Base class for all menu entries
    """
    
    def __init__(self, parent, text):
        self._parent = parent
        self._text = text
        self._highlighted = False
    
    @property
    def highlighted(self):
        return self._highlighted
    
    def highlight(self, highlight=True):
        self._highlighted = highlight
    
    def render(self, draw, xy, *args, **kwargs):
        if args:
            text = self._text.format_map(args[0])
        else:
            text = self._text
        if self._highlighted:
            textsize = draw.textsize(text, self._parent.view.font)[0]
            draw.rectangle((xy[0], xy[1], xy[0]+textsize, xy[1]+self._parent._linesize), fill="white")  # white rectangle titlebar
            draw.text(xy, text, font=self._parent.view.font, fill="black")
        else:
            draw.text(xy, text, font=self._parent.view.font, fill="white")


class MenuCommand(MenuText):
    def __init__(self, parent, text, command=None, callback_args=None):
        super().__init__(parent, text)
        self._command = command
    
    def call_command(self, event):
        self._command(event)
