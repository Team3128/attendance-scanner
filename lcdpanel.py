from threading import Timer
import Adafruit_CharLCD as LCD

lcdPanel = LCD.Adafruit_CharLCDPlate()

timer = Timer()
timeout = 0.0

class LCDPanel:
    def __init__(self, timeout):
        clear_screen()
        self.timeout = timeout

    def clear_screen():
        lcdPanel.clear()
        lcdPanel.set_backlight(0)

    def display(message):
        clear_screen()
        lcdPanel.set_backlight(1)
        lcdPanel.message(message)

    def reset_timer():
        timer = Timer(timeout, clear_screen)
        timer.start()

    def cancel_timer():
        timer.cancel()
