import os

import re
import subprocess

from datetime import datetime

class ButtonApps():
    def __init__(self, lcd_panel, new_scans_path):
        self.lcd_panel = lcd_panel
        self.new_scans_path = new_scans_path

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