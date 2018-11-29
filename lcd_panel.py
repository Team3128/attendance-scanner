import queue
from queue import Queue
from threading import Thread
import time

from i_lcd_panel import ILCDPanel

import Adafruit_CharLCD as LCD

class LCDPanel:
    def __init__(self, cmd_q, data_q):
        self.cmd_q = cmd_q
        self.data_q = data_q

        self.lcd_thread = Thread(target=self.lcd_loop, name="lcd_loop")
        self.lcd_thread.start()

    def lcd_loop(self):
        self.lcd = ILCDPanel()
        clear_time = None
        
        while True:
            if clear_time != None and time.time() > clear_time:
                self.lcd.clear_screen()
                
            try:
                cmd = self.cmd_q.get(False)
                cmd_type = type(cmd).__name__

                if cmd_type == 'DisplayCMD':
                    self.lcd.display(cmd.message)
                    if cmd.timeout > 0:
                        clear_time = time.time() + cmd.timeout

                elif cmd_type == 'ClearScreenCMD':
                    self.lcd.clear_screen()

                elif cmd_type == 'ResetTimerCMD':
                    self.lcd.reset_timer(cmd.timeout)

                elif cmd_type == 'CancelTimerCMD':
                    self.lcd.cancel_timer()

                self.cmd_q.task_done()

            except queue.Empty:
                pass

            up = self.lcd.button_pressed(LCD.UP)
            right = self.lcd.button_pressed(LCD.RIGHT)
            down = self.lcd.button_pressed(LCD.DOWN)
            left = self.lcd.button_pressed(LCD.LEFT)

            select = self.lcd.button_pressed(LCD.SELECT)

            self.data_q.put(ButtonDATA(up, right, down, left, select))
            time.sleep(0.01)

class DisplayCMD:
    def __init__(self, message, timeout = -1):
        self.message = message
        self.timeout = timeout

class ClearScreenCMD:
    def __init__(self):
        pass

class ResetTimerCMD:
    def __init__(self, timeout):
        self.timeout = timeout

class CancelTimerCMD:
    def __init__(self):
        pass


class ButtonDATA:
    def __init__(self, up, right, down, left, select):
        self.up = up
        self.right = right
        self.down = down
        self.left = left

        self.select = select