from threading import Timer
import Adafruit_CharLCD as LCD

lcdPanel = LCD.Adafruit_CharLCDPlate()

timer = Timer(3.0, None)
timeout = 0.0

class LCDPanel:
    def __init__(self, timeout):
        lcdPanel.clear()
        lcdPanel.set_backlight(0)
        self.timeout = timeout

    def clear_screen(self):
        lcdPanel.clear()
        lcdPanel.set_backlight(0)

    def display(self, message):
        self.clear_screen()
        lcdPanel.set_backlight(1)
        lcdPanel.message(message)

    def reset_timer(self):
        timer = Timer(timeout, clear_screen)
        timer.start()

    def cancel_timer(self):
        timer.cancel()
