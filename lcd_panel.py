from threading import Timer

import Adafruit_CharLCD as LCD

class LCDPanel:
    def __init__(self):
        self.adafruit_lcd = LCD.Adafruit_CharLCDPlate()

        self.adafruit_lcd.clear()
        self.adafruit_lcd.set_backlight(0)

        self.message = None
        self.timeout = -1

        self.timer = Timer(0, None)

        self.watcher_thread = Thread(target=self.watcher_loop, name="watcher_loop")
        self.watcher_thread.start()
    
    def sel_button_pressed(self):
        return self.adafruit_lcd.is_pressed(LCD.SELECT)

    def up_button_pressed(self):
        return self.adafruit_lcd.is_pressed(LCD.UP)

    def down_button_pressed(self):
        return self.adafruit_lcd.is_pressed(LCD.DOWN)

    def right_button_pressed(self):
        return self.adafruit_lcd.is_pressed(LCD.RIGHT)
    
    def clear_screen(self):
        self.adafruit_lcd.clear()
        self.adafruit_lcd.set_backlight(0)

    def display(self, message, timeout = -1):
        self.message = message
        self.timeout = timeout

    def watcher_loop(self):
        while True:
            if self.message != None:
                self.lcd_display(self.message, self.timeout)

                self.message = None

    def lcd_display(self, message, timeout = -1):
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
