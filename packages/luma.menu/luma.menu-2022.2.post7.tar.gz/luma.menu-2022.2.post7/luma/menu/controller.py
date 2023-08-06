# -*- coding: utf-8 -*-
import logging
from threading import Event

from luma.menu.model import Model
from luma.menu.view import View
from luma.menu.widgets.menu import MenuCommand

class Controller:
    def __init__(self, ui, display, controls):
        self.logger = logging.getLogger(__name__)
        self._exit = Event()
        
        # @todo should this be turned into state constants?
        self._active = False
        self._interactive = False
        self._locked = False
        self._sleeping = False
        
        self.ui = ui
        self.display = display
        self.controls = controls
        
        # Default blank model/view
        self.model = Model()
        self.view = View(self)
    
    def _register_callbacks(self):
        self.controls.add_event_callback('buttons_ab_held', self.toggle_lock)
        self.controls.add_event_callback('buttons_abc_held', self.toggle_sleep)
        self.controls.add_event_callback('button_a_pressed', self.button_a_pressed)
        self.controls.add_event_callback('button_b_pressed', self.button_b_pressed)
        self.controls.add_event_callback('left_joystick_pressed', self.left_joystick_pressed)
        self.controls.add_event_callback('right_joystick_pressed', self.right_joystick_pressed)
        self.controls.add_event_callback('up_joystick_pressed', self.up_joystick_pressed)
        self.controls.add_event_callback('down_joystick_pressed', self.down_joystick_pressed)
    
    @property
    def is_active(self):
        return self._active
    
    @property
    def is_interactive(self):
        return self._interactive
    
    @property
    def is_locked(self):
        return self._locked
    
    @property
    def is_sleeping(self):
        return self._sleeping

    def button_a_pressed(self):
        if self.is_active:
            if self.is_interactive:
                current_entry = self.view.menu.current_highlighted_entry()
                current_entry.call_command("button_a_pressed")
            else:
                # @todo doesn't highlight first option on current page, but changes page to where 0 is
                # @todo make a method that's view.highlight_current_page() or something? heh
                if self.view.menu.highlightable:
                    self.interactive()
                    self.view.title.highlight()
    
    def button_b_pressed(self):
        if self.is_active:
            if self.is_interactive:
                if not self.view.main_menu.hidden:
                    # Switch to non-interactive only from top menu
                    self.interactive(False)
                    self.view.title.highlight(False)
                else:
                    self.view.show_previous_menu()
    
    def left_joystick_pressed(self):
        if self.is_active:
            if not self.is_interactive:
                self.ui.swipe_left()
    
    def right_joystick_pressed(self):
        if self.is_active:
            if not self.is_interactive:
                self.ui.swipe_right()
    
    def up_joystick_pressed(self):
        if self.is_active:
            if self.is_interactive:
                self.view.menu.highlight_up()
            else:
                self.view.menu.page_up()
    
    def down_joystick_pressed(self):
        if self.is_active:
            if self.is_interactive:
                self.view.menu.highlight_down()
            else:
                self.view.menu.page_down()
    
    def active(self, active=True):
        self._active = active
        if active:
            #self.logger.debug("Registering callbacks...")
            self._register_callbacks()
            #self.logger.debug("Clearing our exit event...")
            self._exit.clear()
        else:
            #self.logger.debug("Clearing callbacks...")
            self.controls.clear_by_obj(self)
            #self.logger.debug("Exiting controller...")
            self._exit.set()
    
    def interactive(self, interactive=True):
        self._interactive = interactive

    def toggle_lock(self):
        if self._locked:
            self.lock(False)
        else:
            self.lock(True)
    
    def lock(self, lock=True):
        self._locked = lock
        self.view.lock()
        self.view.force_redraw()  # Should we force_update rather? in case there isn't a check for should_redraw
    
    def toggle_sleep(self):
        print("sleep toggle called")
        if self._sleeping:
            self.sleep(False)
        else:
            self.sleep(True)
    
    def sleep(self, sleep=True):
        """
        Locks controls and switches the display mode OFF, putting the device in low-power sleep mode
        """
        if sleep:
            self.display.device.hide()
            self.lock()
        else:
            self.display.device.show()
        self._sleeping = sleep
    
    def draw_view(self):
        self.view.update()

    def exit(self):
        self.active(False)
    
    def main(self):
        self.active(True)
        self.view.force_redraw()
        
        while not self._exit.is_set():
            if self.view.should_redraw():
                self.draw_view()
            
            # Wait while we aren't refreshing, greatly reduces CPU usage
            self._exit.wait(self.view.interval)