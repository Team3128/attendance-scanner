import sys
import os

import time
from datetime import datetime

class RecordProccessor:
    def __init__(self, new_scans_path):
        self.new_scans_path = new_scans_path

    def process_data(self, output_path, start_date_str, end_date_str, should_hash):
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        hours = {}

        with open(self.new_scans_path, 'r') as new_scans_file:
            for row in new_scans_file.readlines():
                cells = row.split(',')

                if cells[0] == 'id':
                    continue

                sign_date = datetime.strptime(cells[1], '%Y-%m-%d').date()
                sign_in_time = datetime.strptime(cells[1], '%H:%M:%S.%f').time()

                if sign_date < start_date.date():
                    continue

                if sign_date > end_date.date():
                    continue

                try:
                    sign_out_time = datetime.strptime(cells[2], '%H:%M:%S.%f').time()
                except:
                    continue

                student_id = cells[0]
                if student_id not in hours:
                    hours[student_id] = 0

                hours[student_id] += round((sign_out_time - sign_in_time).total_seconds()/3600, 4)

            sorted_ids = sorted(hours, key=hours.get)

            with open(output_path, 'w') as output_file:
                for student_id in sorted_ids:
                    if should_hash == True:
                        output_file.write("{},{}\n".format(student_id[-4:], round(hours[student_id], 4)))
                    else:
                        output_file.write("{},{}\n".format(student_id, round(hours[student_id], 4)))