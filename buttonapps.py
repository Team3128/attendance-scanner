import sys
import time
from datetime import datetime
import time
import getch
import os
import csv

from lcdpanel import LCDPanel
lcd = LCDPanel(10.0)

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

scansFileRelPath = "scans.csv"
scansFileAbsPath = os.path.join(script_dir, scansFileRelPath)

print("Button apps starting up...")

while 1 == 1:
    if lcd.lcdPanel.is_pressed(LCD.SELECT):
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

        lcd.display(str(signedin) + " people\nsigned in now.")
        lcd.resetTimer()
