import sys
import os

from threading import Thread

import time
from datetime import datetime

from lcd_panel import LCDPanel
from scan_logger import BarcodeBuffer
from scan_logger import ScanLogger
from button_apps import ButtonApps
from report_generator import ReportGenerator

import evdev
from evdev import ecodes

new_scans_path = "newscans.csv"

season = "2018-19"

total_start = "2018-09-07"
total_end = "2019-06-14"

build_start = "2019-01-05"
build_end = "2019-02-19"

class AttendanceScanner:
    def __init__(self):
        self.lcd_panel = LCDPanel()

        self.lcd_panel.display("Connecting\nto reader...")

        self.reader = None
        while self.reader == None:
            for dev in [evdev.InputDevice(fn) for fn in evdev.list_devices()]:
                if dev.name == "Barcode Reader ":
                    self.reader = dev

        self.lcd_panel.display("Reader connected.", 2)

        self.barcode_buffer = BarcodeBuffer()
        self.scan_logger = ScanLogger(new_scans_path)
        self.button_apps = ButtonApps(self.lcd_panel, new_scans_path)
        self.report_generator = ReportGenerator(new_scans_path, season, total_start, total_end, build_start, build_end)

    def reader_loop(self):
        for event in self.reader.read_loop():
            barcode = self.barcode_buffer.process_event(event)

            if barcode == None:
                continue

            self.barcode_buffer.flush()
            
            hours = self.scan_logger.log_scan(barcode)

            if hours == "":
                self.lcd_panel.display("Signed in\n{}".format(barcode), 5)
            else:
                self.lcd_panel.display("{}\n{}".format(barcode, hours), 5)

    def button_loop(self):
        while True:
            self.button_apps.poll_buttons()
            time.sleep(0.01)

    def report_generation_loop(self):
        previous_date = datetime.now().date()

        while True:
            current_date = datetime.now().date()

            if current_date != previous_date :
                previous_date = current_date

                self.report_generator.update()

            time.sleep(30.0)

    def run(self):
        print("Running Attendance Scanner.")

        self.reader_thread = Thread(target=self.reader_loop, name="Reader Loop")
        self.reader_thread.start()
        
if __name__ == '__main__':
    scan = AttendanceScanner()
    scan.run()