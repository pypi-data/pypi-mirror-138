# -*- coding: utf-8 -*-
import logging
import inspect
from threading import Event

from luma.menu.controller import Controller

class UserInterface:
    def __init__(self, display, controls):
        self.logger = logging.getLogger(__name__)
        self.exit = Event()
        
        self._controllers = list()
        self._ctrl = None
        self._active_ctrl = None
        
        self._display = display
        self._controls = controls
    
    def add_controller(self, controllers):
        # Convert singular passed controller to a tuple before iteration
        if not isinstance(controllers, list) and not isinstance(controllers, tuple):
                controllers = [controllers]
        for controller in controllers:
            # Ensure as much as reasonably possible that this is a valid controller
            if (inspect.isclass(controller)) and (Controller in controller.__bases__):
                self._controllers.append(controller(self, self._display, self._controls))
            else:
                raise ValueError(f"Passed argument not a valid controller: {controller} in {controllers}")
        if (self._active_ctrl is None) and len(self._controllers):
            self._active_ctrl = 0
    
    def swipe_right(self):
        """
        Increase active controller, emulates scrolling right
        """
        prev_ctrl = self._active_ctrl
        if self._active_ctrl == 0:
            self._active_ctrl = len(self._controllers)-1
        else:
            self._active_ctrl -= 1
        if self._active_ctrl != prev_ctrl:
            self._ctrl.exit()
    
    def swipe_left(self):
        """
        Decrease active controller, emulates scrolling left
        """
        prev_ctrl = self._active_ctrl
        if self._active_ctrl == (len(self._controllers)-1):
            self._active_ctrl = 0
        else:
            self._active_ctrl += 1
        if self._active_ctrl != prev_ctrl:
            self._ctrl.exit()
    
    def main(self):
        if self._active_ctrl is None:
            self.logger.info("No controller available, exiting...")
            return
        try:
            while not self.exit.is_set():
                self._ctrl = self._controllers[self._active_ctrl]
                self._ctrl.main()
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received, exiting...")
