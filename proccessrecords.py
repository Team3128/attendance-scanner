import sys
import time
import getch
import os
import csv
from datetime import datetime

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

scansFileRelPath = "scans.csv"
scansFileAbsPath = os.path.join(script_dir, scansFileRelPath)

tempFileRelPath = "tmp_data/temp.csv"
tempFileAbsPath = os.path.join(script_dir, tempFileRelPath)

hoursFileRelPath = str(sys.argv[1])
hoursFileAbsPath = os.path.join(script_dir, hoursFileRelPath)

startDate = sys.argv[2]

shouldHash = sys.argv[3]

open(tempFileAbsPath, 'w').close()

with open(scansFileAbsPath, 'r') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames = ['id', 'timein', 'timeout'])

    open(hoursFileRelPath, 'w').close()

    ids = []
    hours = []

    for row in reader:
        if row['timeout'] != "" and row['id'] != "id" and datetime.strptime(row['timein'], '%Y-%m-%d %H:%M:%S.%f') > datetime.strptime(startDate + " 00:00:00.000000", '%Y-%m-%d %H:%M:%S.%f'):
            found = False
            for code in ids:
                if code == row['id']:
                    found = True

            if found == False:
                ids.append(row['id'])
                hours.append(0.0)

            timein = datetime.strptime(row['timein'], '%Y-%m-%d %H:%M:%S.%f')
            timeout = datetime.strptime(row['timeout'], '%Y-%m-%d %H:%M:%S.%f')

            with open(tempFileAbsPath, 'a') as temp:
                temp.write(row['id'] + ", " + str(round((timeout - timein).total_seconds()/3600, 4)) + "\n")

    for index, barcode in enumerate(ids):
        with open(tempFileAbsPath, 'r') as tempfile:
            reader = csv.DictReader(tempfile, fieldnames = ['id', 'hours'])
            for row in reader:
                if row['id'] == barcode:
                    hours[index] = hours[index] + float(row['hours'])

    with open(hoursFileAbsPath, 'w') as hoursfile:
        for index, barcode in enumerate(ids):
            if shouldHash == "hash=true":
                hoursfile.write(barcode[-4:] + ", " + str(round(hours[index], 4)) + "\n")
            else:
                hoursfile.write(barcode + ", " + str(round(hours[index], 4)) + "\n")

os.remove(tempFileAbsPath)
