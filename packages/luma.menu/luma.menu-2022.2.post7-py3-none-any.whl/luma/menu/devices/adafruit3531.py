import logging

from gpiozero import Button
from luma.menu import Controls

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

"""
Adafruit 128x64 OLED Bonnet for Raspberry Pi
Product ID: 3531
https://www.adafruit.com/product/3531
"""

class Display:
    def __init__(self, port=1, address=0x3C, contrast=None):
        """
        Default port, address support:
        - Raspberry Pi Zero W Rev 1.1 (Bullseye)
        - Raspberry Pi 4 Model B Rev 1.1 (Bullseye)
        """
        self.logger = logging.getLogger(__name__)
        
        self.logger.debug(f"Display settings: port={port}, address={hex(address)}")
        serial = i2c(port=port, address=address)
        self.device = ssd1306(serial)
        
        if contrast:
            self.logger.debug(f"Changing contrast level to {contrast}")
            self.device.contrast(contrast)

class Controls(Controls):
    def __init__(self, buttons=(5,6,4,27,23,17,22)):
        """
        Buttons list order:
        (button #5, button #6, button center of joystick, left, right, up, down)
        
        Default buttons support:
        - Raspberry Pi Zero W Rev 1.1 (Bullseye)
        - Raspberry Pi 4 Model B Rev 1.1 (Bullseye)
        """
        super().__init__()
        
        # Additional attribute for all buttons
        Button.was_held = False
        
        self.button_A = Button(buttons[0], pull_up=True, hold_time=2)  # Button #5
        self.button_B = Button(buttons[1], pull_up=True, hold_time=2)  # Button #6
        self.button_C = Button(buttons[2], pull_up=True, hold_time=3)  # Button Center of Joystick
        self.button_L = Button(buttons[3], pull_up=True, hold_time=1, hold_repeat=True)  # Left (Joystick)
        self.button_R = Button(buttons[4], pull_up=True, hold_time=1, hold_repeat=True)  # Right (Joystick)
        self.button_U = Button(buttons[5], pull_up=True, hold_time=1, hold_repeat=True)  # Up (Joystick)
        self.button_D = Button(buttons[6], pull_up=True, hold_time=1, hold_repeat=True)  # Down (Joystick)
        self.button_A.when_held = self._held
        self.button_B.when_held = self._held
        self.button_C.when_held = self._held
        self.button_L.when_held = self._held
        self.button_R.when_held = self._held
        self.button_U.when_held = self._held
        self.button_D.when_held = self._held
        self.button_L.when_pressed = lambda: self._event('left_joystick_pressed')
        self.button_R.when_pressed = lambda: self._event('right_joystick_pressed')
        self.button_U.when_pressed = lambda: self._event('up_joystick_pressed')
        self.button_D.when_pressed = lambda: self._event('down_joystick_pressed')
        # When using when_held, simulate a "pressed" event using when_released
        # Ref: https://gpiozero.readthedocs.io/en/stable/faq.html#how-do-i-use-button-when-pressed-and-button-when-held-together
        self.button_A.when_released = self._released
        self.button_B.when_released = self._released
        self.button_C.when_released = self._released
        
        self.logger.info("Controls initialized, ready to call events...")

    def _held(self, btn):
        btn.was_held = True
    
        # Call a pressed event, we only use joystick holds for repetitive presses
        if btn in (self.button_L, self.button_R, self.button_U, self.button_D):
            btn.was_held = False
            return btn.when_pressed()
        
        if self.button_A.is_held and self.button_B.is_held and self.button_C.is_held:
            self._event('buttons_abc_held')
            
        elif self.button_A.is_held and self.button_B.is_held:
            self._event('buttons_ab_held')
            
        elif self.button_A.is_held:
            self._event('button_a_held')
            
        elif self.button_B.is_held:
            self._event('button_b_held')
            
        elif self.button_C.is_held:
            self._event('button_c_held')
            
        else:
            self.logger.warning(f"Unknown button held: {btn}")
    
    def _released(self, btn):
        # When using when_held, simulate a "pressed" event using when_released
        # Ref: https://gpiozero.readthedocs.io/en/stable/faq.html#how-do-i-use-button-when-pressed-and-button-when-held-together
        if not btn.was_held:
            if btn is self.button_A:
                self._event('button_a_pressed')
            elif btn is self.button_B:
                self._event('button_b_pressed')
            elif btn is self.button_C:
                self._event('button_c_pressed')
        
        # Reset
        btn.was_held = False
