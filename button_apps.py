import os
import subprocess

import re
import time

from datetime import datetime

from lcd_panel import ButtonDATA
from lcd_panel import DisplayCMD
from lcd_panel import ClearScreenCMD

class ButtonApps():
    def __init__(self, new_scans_path, cmd_q):
        self.new_scans_path = new_scans_path

        self.cmd_q = cmd_q

        self.rebooting = False

    def poll_buttons(self, button_data):
        if button_data.select:
            signed_in = 0

            current_date = datetime.now().date()

            with open(self.new_scans_path, 'r') as new_scans_file:
                for row in new_scans_file.read().splitlines():
                    cells = row.split(',') 
                    
                    sign_date = datetime.strptime(cells[1], '%Y-%m-%d').date()

                    # Did the student sign in today?
                    if sign_date != current_date:
                        continue

                    # Is the student still signed in?
                    if cells[3].strip() != "":
                        continue

                    signed_in += 1

            self.cmd_q.put(DisplayCMD("{} people\nsigned in now.".format(signed_in), 5))

        if button_data.up:
            self.cmd_q.put(DisplayCMD("Reboot? Press\nDOWN to confirm."))
            self.rebooting = True

            time.sleep(5)

            self.cmd_q.put(ClearScreenCMD())
            self.rebooting = False

        if button_data.down:
            if self.rebooting:
                self.cmd_q.put(DisplayCMD("Rebooting..."))
                time.sleep(2)
                
                os.system('reboot')