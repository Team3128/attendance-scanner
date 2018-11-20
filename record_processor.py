import sys
import os

import time
from datetime import datetime

class RecordProccessor:
    def __init__(self, scans_path):
        self.scans_path = scans_path

    def process_data(self, output_path, start_date_str, end_date_str, should_hash):
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        hours = {}

        with open(self.scans_path, 'r') as scans_file:
            for row in scans_file.readlines():
                cells = row.strip().split(',')

                if len(cells) <= 1:
                    continue

                if cells[0] == 'id':
                    continue

                sign_date = datetime.strptime(cells[1], '%Y-%m-%d').date()
                sign_in_time = datetime.strptime(cells[2], '%H:%M:%S.%f').time()

                if sign_date < start_date.date():
                    continue

                if sign_date > end_date.date():
                    continue

                try:
                    sign_out_time = datetime.strptime(cells[3], '%H:%M:%S.%f').time()
                    student_id = cells[0]
                except:
                    continue
                    
                if student_id not in hours:
                    hours[student_id] = 0

                hours[student_id] += round((datetime.combine(sign_date, sign_out_time) - datetime.combine(sign_date, sign_in_time)).total_seconds()/3600, 4)

            sorted_ids = sorted(hours, key=hours.get, reverse=True)

            with open(output_path, 'w') as output_file:
                if should_hash:
                    output_file.write("Student ID (last 4 digits), Hours\n")
                else:
                    output_file.write("Student ID, Hours\n")

                for student_id in sorted_ids:
                    if should_hash == True:
                        output_file.write("{},{}\n".format(student_id[-4:], round(hours[student_id], 4)))
                    else:
                        output_file.write("{},{}\n".format(student_id, round(hours[student_id], 4)))