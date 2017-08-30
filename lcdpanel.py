from threading import Timer
import Adafruit_CharLCD as LCD

lcdPanel = LCD.Adafruit_CharLCDPlate()

timer = Timer(3.0, None)
timeout = 3.0

class LCDPanel:
    def __init__(self, timeout):
        lcdPanel.clear()
        lcdPanel.set_backlight(0)
        self.timeout = timeout

    def reset(self):
        lcdPanel = LCD.Adafruit_CharLCDPlate()
    
    def sel_button_pressed(self):
        return lcdPanel.is_pressed(LCD.SELECT)

    def up_button_pressed(self):
        return lcdPanel.is_pressed(LCD.UP)

    def down_button_pressed(self):
        return lcdPanel.is_pressed(LCD.DOWN)

    def right_button_pressed(self):
        return lcdPanel.is_pressed(LCD.RIGHT)
    
    def clear_screen(self):
        lcdPanel.clear()
        lcdPanel.set_backlight(0)

    def display(self, message):
        self.clear_screen()
        lcdPanel.set_backlight(1)
        lcdPanel.message(message)

    def reset_timer(self):
        self.cancel_timer()
        timer = Timer(self.timeout, self.clear_screen)
        timer.start()

    def cancel_timer(self):
        timer.cancel()
