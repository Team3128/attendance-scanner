import time
from datetime import datetime

import os

import evdev
from evdev import ecodes

class BarcodeBuffer:
    def __init__(self):
        self.barcode = ""

    def process_event(self, event):
        if event.type != evdev.ecodes.EV_KEY:
            return None

        key = "a"
        if event.value == 1:
            key = evdev.ecodes.KEY[event.code][4:]

        if key.isdigit():
            self.barcode += key

        if key == "SPACE":
            return self.barcode

        return None

    def flush(self):
        self.barcode = ""

class ScanLogger:
    def __init__(self, new_scans_path):
        self.barcode = ""
        self.new_scans_path = new_scans_path

    def log_scan(self, student_id):
        if len(student_id) < 5:
            return None

        current_date = datetime.now().date()
        current_time = datetime.now().time()

        sign_in_line = -1

        open(self.new_scans_path, 'a').close()

        with open(self.new_scans_path, 'r') as new_scans_file:
            # Searching the new scans file to determine if the student is signing out
            for line, row in enumerate(new_scans_file.read().splitlines()):
                cells = row.split(',')

                # Does the row actually correspond to this student?
                if cells[0] != student_id:
                    continue

                sign_in_date = datetime.strptime(cells[1], '%Y-%m-%d').date()
                sign_in_time = datetime.strptime(cells[2], '%H:%M:%S.%f').time()

                # Did the student sign in today?
                if sign_in_date != current_date:
                    continue

                # Is the student still signed in?
                if cells[3].strip() != "":
                    continue

                # If we get to this point, this row corresponds to the student having signed in earlier today and not yet signed out.
                sign_in_line = line
                break

        # The student is signing out.
        if sign_in_line != -1:
            logs = []

            # Filling logs with the current lines
            with open(self.new_scans_path, 'r') as new_scans_file:
                logs = new_scans_file.read().splitlines()

            # Adding the sign-out time to the line containing the corresponding sign-in
            logs[sign_in_line] = logs[sign_in_line].strip() + str(current_time)

            # Writing the adjusted lines back to the file
            with open(self.new_scans_path, 'w') as new_scans_file:
                for log in logs:
                    new_scans_file.write(log.strip() + '\n')

            total_time = datetime.combine(current_date, current_time) - datetime.combine(current_date, sign_in_time)

            return "{}hr {}min".format(total_time.seconds//3600, (total_time.seconds//60)%60)

        # The student is signing in.
        else:
            with open(self.new_scans_path, 'a') as new_scans_file:
                new_scans_file.write(("{},{},{},\n").format(student_id, current_date, current_time))

            return ""
