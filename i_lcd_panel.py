from threading import Timer

import Adafruit_CharLCD as LCD

class ILCDPanel:
    def __init__(self):
        self.adafruit_lcd = LCD.Adafruit_CharLCDPlate()

        self.adafruit_lcd.clear()
        self.adafruit_lcd.set_backlight(0)

        self.timer = Timer(0, None)
    
    def button_pressed(self, button):
        return self.adafruit_lcd.is_pressed(button)
    
    def clear_screen(self):
        self.adafruit_lcd.clear()
        self.adafruit_lcd.set_backlight(0)

    def display(self, message, timeout = -1):
        self.adafruit_lcd.clear()
        
        self.adafruit_lcd.set_backlight(1)
        self.adafruit_lcd.message(message)

        if timeout >= 0:
            self.reset_timer(timeout)

    def reset_timer(self, timeout):
        self.cancel_timer()

        self.timer = Timer(timeout, self.clear_screen)
        self.timer.start()

    def cancel_timer(self):
        self.timer.cancel()
