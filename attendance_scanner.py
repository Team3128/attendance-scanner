import sys
import os
import subprocess

import re

from threading import Thread
from queue import Queue
from queue import Empty

import time
from datetime import datetime

from lcd_panel import LCDPanel

from lcd_panel import DisplayCMD
from lcd_panel import ClearScreenCMD

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
        self.cmd_q = Queue()
        self.data_q = Queue()

        self.lcd_panel = LCDPanel(self.cmd_q, self.data_q)

        self.cmd_q.put(DisplayCMD("Attendance\nScanner v2.3.4"))
        time.sleep(3)

        self.cmd_q.put(DisplayCMD("Connecting\nto reader..."))

        self.reader = None
        while self.reader == None:
            for dev in [evdev.InputDevice(fn) for fn in evdev.list_devices()]:
                if dev.name == "Barcode Reader ":
                    self.reader = dev

        self.cmd_q.put(DisplayCMD("Reader connected."))

        self.barcode_buffer = BarcodeBuffer()
        self.scan_logger = ScanLogger(new_scans_path)
        self.button_apps = ButtonApps(new_scans_path, self.cmd_q)
        self.report_generator = ReportGenerator(new_scans_path, season, total_start, total_end, build_start, build_end)

        time.sleep(2)

    def reader_loop(self):
        for event in self.reader.read_loop():
            barcode = self.barcode_buffer.process_event(event)

            if barcode == None:
                continue

            self.barcode_buffer.flush()
            
            hours = self.scan_logger.log_scan(barcode)

            if hours == "":
                self.cmd_q.put(DisplayCMD("Signed in\n{}".format(barcode), 5))
            else:
                self.cmd_q.put(DisplayCMD("{}\n{}".format(barcode, hours), 5))

    def button_loop(self):
        while True:
            try:
                button_data = self.data_q.get(False)
                self.button_apps.poll_buttons(button_data)
            except Empty:
                pass
            except:
                self.cmd_q.put(DisplayCMD("ERROR: Button\nApp Failed.", 3))
                
            time.sleep(0.01)

    def report_loop(self):
        previous_date = datetime.now().date()

        while True:
            current_date = datetime.now().date()

            if current_date != previous_date :
                previous_date = current_date

                self.cmd_q.put(DisplayCMD("Processing...\nDO NOT SCAN"))
                self.report_generator.update()
                self.cmd_q.put(ClearScreenCMD())

            time.sleep(1800)

    def run(self):
        print("Running Attendance Scanner.")

        self.cmd_q.put(DisplayCMD("Checking\ninternet..."))

        attempts = 0
        while attempts < 10:
            try:
                match = re.search('inet addr', subprocess.check_output('ifconfig wlan0', shell=True))
                break
            except Exception:
                attempts += 1

        if attempts >= 10:
            self.cmd_q.put(DisplayCMD("Wi-Fi Error.\nPlease reboot."))
            return None

        self.cmd_q.put(DisplayCMD("Internet\nConnected.", 2))

        self.reader_thread = Thread(target=self.reader_loop, name="reader_loop")
        self.reader_thread.start()

        self.button_thread = Thread(target=self.button_loop, name="button_loop")
        self.button_thread.start()

        self.report_thread = Thread(target=self.report_loop, name="report_loop")
        self.report_thread.start()

        
if __name__ == '__main__':
    scan = AttendanceScanner()
    scan.run()