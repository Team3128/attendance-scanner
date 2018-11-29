from threading import Timer

import Adafruit_CharLCD as LCD

class ILCDPanel:
    def __init__(self):
        self.adafruit_lcd = LCD.Adafruit_CharLCDPlate()

        self.adafruit_lcd.clear()
        self.adafruit_lcd.set_backlight(0)
    
    def button_pressed(self, button):
        return self.adafruit_lcd.is_pressed(button)
    
    def clear_screen(self):
        self.adafruit_lcd.clear()
        self.adafruit_lcd.set_backlight(0)

    def display(self, message):
        self.adafruit_lcd.clear()
        
        self.adafruit_lcd.set_backlight(1)
        self.adafruit_lcd.message(message)