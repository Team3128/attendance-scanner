import os
import subprocess

import re
import time

from datetime import datetime

class ButtonApps():
    def __init__(self, lcd_panel, new_scans_path):
        self.lcd_panel = lcd_panel
        self.new_scans_path = new_scans_path

        self.rebooting = False

    def poll_buttons(self):
        if self.lcd_panel.sel_button_pressed():
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

            self.lcd_panel.display("{} people\nsigned in now.".format(signed_in))

        if self.lcd_panel.up_button_pressed():
            self.lcd_panel.display("Reboot? Press\nDOWN to confirm.")
            self.rebooting = True

            time.sleep(5)

            self.lcd_panel.clear_screen()
            self.rebooting = False

        if self.lcd_panel.down_button_pressed():
            if self.rebooting:
                self.lcd_panel.display("Rebooting...")
                time.sleep(2)
                
                os.system('reboot')