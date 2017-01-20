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

lastScanRelPath = "lastscan.txt"
lastScanAbsPath = os.path.join(script_dir, lastScanRelPath)

barcode = ""
totaltime = 0

def clearScreen():
    lcd.clear()
    lcd.set_backlight(0)

timer = Timer(3.0, clearScreen)
clearScreen()

lcd.set_backlight(1)
lcd.message("Attendance\nScanner v2.0")
while 1 == 1 :
    # MARK: Get member barcode and put it in the records CSV
    char = getch.getch()
    if char != " " :
        if char[:1].isdigit() :
            barcode += char
    else :
        if len(barcode) > 4:
            timer.cancel()
            currenttime = datetime.today()

            with open(scansFileAbsPath, 'r') as csvfile:
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
                            with open(scansFileAbsPath, 'rb') as b:
                                bottles = csv.reader(b)
                                bottle_list.extend(bottles)

                            # data to override in the format {line_num_to_override:data_to_write}.
                            line_to_override = {rownum:[row['id'], str(firsttime) ,str(nowtime)] }

                            # Write data to the csv file and replace the lines in the line_to_override dict.
                            with open(scansFileAbsPath, 'wb') as b:
                                writer = csv.writer(b)
                                for line, row1 in enumerate(bottle_list):
                                    data = line_to_override.get(line, row1)
                                    writer.writerow(data)

                lcd.set_backlight(1);
                lcd.clear();
                if found == False :
                    with open(scansFileAbsPath, 'a') as scansFile:
                        scansFile.write(barcode) #Barcode
                        scansFile.write(",")
                        scansFile.write(str(currenttime)) #Local time
                        scansFile.write(",")
                        scansFile.write(" ")
                        scansFile.write("\n")

                    lcd.message("Signed in\n" + barcode)

                else:
                    timething = datetime.strptime(str(totaltime), '%H:%M:%S.%f')
                    lcd.message(barcode + "\n" + str(timething.hour) + "hr " + str(timething.minute) + "min")
            timer = Timer(3.0, clearScreen)
            timer.start()
        barcode = ""
