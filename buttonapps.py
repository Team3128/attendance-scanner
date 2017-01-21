import sys
import time
from datetime import datetime
import time
import getch
import os
import csv
from threading import Timer

import Adafruit_CharLCD as LCD
lcd = LCD.Adafruit_CharLCDPlate()

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

scansFileRelPath = "scans.csv"
scansFileAbsPath = os.path.join(script_dir, scansFileRelPath)

def clearScreen():
    lcd.clear()
    lcd.set_backlight(0)

def display(message):
    clearScreen()
    lcd.set_backlight(1)
    lcd.message(message)
    reset_timer()

def reset_timer():
    timer = Timer(3.0, clearScreen)
    timer.start()

timer = Timer(10.0, clearScreen)
clearScreen()

print("Number people signed in widget")

while 1 == 1:
    if lcd.is_pressed(LCD.SELECT):
        signedin = 0
        with open(scansFileAbsPath, 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames = ['id', 'timein', 'timeout'])

            ids = []

            for row in reader:
                if row['timeout'] == " ":
                    firsttime = datetime.strptime(row['timein'], '%Y-%m-%d %H:%M:%S.%f')
                    nowtime = datetime.strptime(str(datetime.today()), '%Y-%m-%d %H:%M:%S.%f')

                    if firsttime.date() == nowtime.date():
                        if row['id'] in ids:
                            rand=0
                        else:
                            ids.append(row['id'])

            signedin = len(ids)

        display(str(signedin) + " people\nsigned in now.")
