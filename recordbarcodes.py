import sys
import time
from datetime import datetime
import time
import getch
import os
import csv

from lcdpanel import LCDPanel
import evdev
from evdev import ecodes

lcd = LCDPanel(3.0)

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

newScansFilePath = os.path.join(script_dir, "newscans.csv")

barcode = ""
totaltime = 0

device = evdev.InputDevice('/dev/input/event0')

for dev in [evdev.InputDevice(fn) for fn in evdev.list_devices()]:
    if dev.name == "Barcode Reader ":
        device = dev

lcd.display("Attendance\nScanner v2.2.0")
print("Attendance Scanner v2.2.0")

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        letter = ""
        if event.value == 01:
            letter = evdev.ecodes.KEY[event.code][4:]
        else:
            letter = "a"
        
        if letter.isdigit():
            barcode += letter
        elif letter == "SPACE":
            if len(barcode) > 4:
                lcd.cancel_timer()
                currenttime = datetime.today()

                with open(newScansFilePath, 'r') as csvfile:
                    reader = csv.DictReader(csvfile, fieldnames = ['id', 'timein', 'timeout'])

                    rownum = -1
                    found = False

                    for row in reader:
                        rownum = rownum + 1
                        if row['id'] == barcode and row['timeout'] == ' ':
                            firsttime = datetime.strptime(row['timein'], '%Y-%m-%d %H:%M:%S.%f')
                            nowtime = datetime.strptime(str(currenttime), '%Y-%m-%d %H:%M:%S.%f')

                            if firsttime.date() == nowtime.date():
                                found = True
                                totaltime = nowtime - firsttime
                                bottle_list = []

                                # Read all data from the csv file.
                                with open(newScansFilePath, 'rb') as b:
                                    bottles = csv.reader(b)
                                    bottle_list.extend(bottles)

                                # data to override in the format {line_num_to_override:data_to_write}.
                                line_to_override = {rownum:[row['id'], str(firsttime) ,str(nowtime)] }

                                # Write data to the csv file and replace the lines in the line_to_override dict.
                                with open(newScansFilePath, 'wb') as b:
                                    writer = csv.writer(b)
                                    for line, row1 in enumerate(bottle_list):
                                        data = line_to_override.get(line, row1)
                                        writer.writerow(data)

                    if found == False:
                        with open(newScansFilePath, 'a') as scansFile:
                            scansFile.write(str(barcode) + "," + str(currenttime) + ", \n")

                        lcd.display("Signed in\n" + barcode)

                    else:
                        hourslogged = datetime.strptime(str(totaltime), '%H:%M:%S.%f')
                        lcd.display(barcode + "\n" + str(hourslogged.hour) + "hr " + str(hourslogged.minute) + "min")
                    lcd.reset_timer()
            barcode = ""
