import sys
import time
import getch
import os
import csv
from datetime import datetime

script_dir = os.path.dirname(__file__)

scansFilePath = os.path.join(script_dir, "scans.csv")
tempFilePath = os.path.join(script_dir, "tmp_data/temp.csv")

class RecordProccess:
    def __init__(self):
        rand = 0

    def proccessData(self, outputFileRelPath, startDateStr, endDateStr, shouldHash):
        outputFilePath = os.path.join(script_dir, outputFileRelPath)

        open(tempFilePath, 'w').close()

        startDate = datetime.strptime(startDateStr + " 00:00:00.000000", '%Y-%m-%d %H:%M:%S.%f')
        endDate = datetime.strptime(endDateStr + " 00:00:00.000000", '%Y-%m-%d %H:%M:%S.%f')

        open(outputFilePath, 'w').close()

        ids = []
        hours = []

        with open(scansFilePath, 'r') as scansFile:
            reader = csv.DictReader(scansFile, fieldnames = ['id', 'timein', 'timeout'])

            for row in reader:
                if row['timeout'] != "" and row['timeout'] != " " and len(row['id']) > 4 and row['id'] != "id" and datetime.strptime(row['timein'], '%Y-%m-%d %H:%M:%S.%f') > startDate and datetime.strptime(row['timein'], '%Y-%m-%d %H:%M:%S.%f') < endDate :
                    found = False
                    for code in ids:
                        if code == row['id']:
                            found = True

                    if found == False:
                        ids.append(row['id'])
                        hours.append(0.0)

                    timein = datetime.strptime(row['timein'], '%Y-%m-%d %H:%M:%S.%f')
                    timeout = datetime.strptime(row['timeout'], '%Y-%m-%d %H:%M:%S.%f')

                    with open(tempFilePath, 'a') as tempfile:
                        tempfile.write(row['id'] + ", " + str(round((timeout - timein).total_seconds()/3600, 4)) + "\n")

            for index, barcode in enumerate(ids):
                with open(tempFilePath, 'r') as tempfile:
                    reader = csv.DictReader(tempfile, fieldnames = ['id', 'hours'])
                    for row in reader:
                        if row['id'] == barcode:
                            hours[index] = hours[index] + float(row['hours'])

            with open(outputFilePath, 'w') as hoursfile:
                for index, barcode in enumerate(ids):
                    if shouldHash == True:
                        hoursfile.write(barcode[-4:] + ", " + str(round(hours[index], 4)) + "\n")
                    else:
                        hoursfile.write(barcode + ", " + str(round(hours[index], 4)) + "\n")

        os.remove(tempFilePath)
