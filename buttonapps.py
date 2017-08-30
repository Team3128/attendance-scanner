import sys
import time
from datetime import datetime
import time
import getch
import os
import csv
import subprocess
import re

from lcdpanel import LCDPanel
lcd = LCDPanel(10.0)

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

lastFilePath = os.path.join(script_dir, "last.txt")
with open(lastFilePath, 'w') as lastfile:
    lastfile.write("NOT")

newScansFile = os.path.join(script_dir, "newscans.csv")

print("Button apps starting up...")

while 1 == 1:
    if lcd.sel_button_pressed():
        lcd.reset()
        signedin = 0
        with open(newScansFile, 'r') as csvfile:
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
        lcd.reset_timer()
    if lcd.up_button_pressed():
        lcd.display("Please wait...")

        os.system("sudo /sbin/ifup --force wlan0")
        
        lcd.clear_screen()
        print("Displayed")
    if lcd.down_button_pressed():
        output = subprocess.check_output('ifconfig wlan0', shell=True)
        try:
            ipaddr = re.search('(?<=10.31.28.)\w+', output)
            lcd.display('IP:\n10.31.28.'+str(ipaddr.group(0)))
        except Exception:
            lcd.display('IP: nope.')
        lcd.reset_timer()
    if lcd.right_button_pressed():
        with open(lastFilePath, 'r') as lastfile:
            lcd.display(lastfile.read())
