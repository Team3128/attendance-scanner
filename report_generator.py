import os
import sys
import shutil

from datetime import datetime
import time

from record_processor import RecordProccessor

from github import Github
from github import Repository

# HASHED FILE PATHS
total_hours_hashed_path = "tmp_data/totalhours_hashed.csv"
build_season_hashed_path = "tmp_data/buildseason_hashed.csv"

# UNHASHED FILE PATHS
total_hours_unhashed_path = "tmp_data/totalhours.csv"
build_season_unhashed_path = "tmp_data/buildseason.csv"

# ENCRYPTED FILE PATHS
total_hours_encrypted_path = total_hours_unhashed_path + ".gpg"
build_season_encrypted_path = build_season_unhashed_path + ".gpg"

# SCANS FILE PATHS
scans_hashed_path = "tmp_data/scans.csv"
scans_unhashed_path = "tmp_data/priv/scans.csv"
scans_encrypted_path = "tmp_data/priv/scans.csv.gpg"

# CONFIG FILE PATHS
private_key_path = "config/privatekey.txt"
gpg_pass_path = "config/gpgpassphrase.txt"

class ReportGenerator:
    def __init__(self, new_scans_path, season, total_start, total_end, build_start, build_end):
        self.new_scans_path = new_scans_path

        with open(private_key_path, 'r') as private_key_file:
            self.g = Github(private_key_file.read())

        for r in self.g.get_user().get_repos():
            if r.name == "{}-attendance-data".format(season):
                self.repo = r

        self.total_start = total_start
        self.total_end = total_end
        self.build_start = build_start
        self.build_end = build_end

        self.record_processor = RecordProccessor(new_scans_path)

    def update(self):
        today_date = str(datetime.date.today())

        shutil.rmtree('tmp_data', ignore_errors=True)

        os.mkdir('tmp_data')
        os.mkdir('tmp_data/priv')
        
        with open(scans_encrypted_path, 'w') as scans_encrypted_file:
            scans_encrypted_file.write(self.repo.get_file_contents('/scans.csv.gpg').decoded_content)

        with open(gpg_pass_path, 'r') as pass_file:
            os.system("echo '" + pass_file.read() + "' | gpg --passphrase-fd 0 -o '" + scans_unhashed_path + "' -d '" + scans_encrypted_path + "'")

        with open(scans_unhashed_path, 'a') as scans_unhashed_file:
            with open(self.new_scans_path, 'r') as new_scans_file:
                for row in new_scans_file.readlines():
                    cells = row.split(',')

                    if cells[0] != 'id':
                        scans_unhashed_file.write(row + '\n')

        os.remove(scans_encrypted_path)

        self.record_processor.process_data(total_hours_hashed_path, self.total_start, self.total_end, True)
        self.record_processor.process_data(build_season_hashed_path, self.build_start, self.build_end, True)

        self.record_processor.process_data(total_hours_unhashed_path, self.total_start, self.total_end, False)
        self.record_processor.process_data(build_season_unhashed_path, self.build_start, self.build_end, False)

        with open(scans_unhashed_path, 'r') as scans_unhashed_file:
            with open(scans_hashed_path, 'w') as scans_hashed_file:
                for row in scans_unhashed_file.readlines():
                    cells = row.split(',')

                    if cells[0] == 'id':
                        continue

                    hashed_student_id = cells[0][-4:]

                    sign_date = datetime.strptime(cells[1], '%Y-%m-%d').date()

                    sign_in_time = datetime.strptime(cells[1], '%H:%M:%S.%f').time()
                    try:
                        sign_out_time = datetime.strptime(cells[2], '%H:%M:%S.%f').time()
                        hours = round((sign_out_time - sign_in_time).total_seconds()/3600, 4)
                    except:
                        sign_out_time = ""
                        hours = 0

                    scans_hashed_file.write("{},{},{},{},{}\n".format(hashed_student_id, sign_date, sign_in_time, sign_out_time, hours))

        os.system("gpg -e -r 'Team 3128' " + scans_unhashed_path)
        os.system("gpg -e -r 'Team 3128' " + total_hours_unhashed_path)
        os.system("gpg -e -r 'Team 3128' " + build_season_unhashed_path)
        

        msg = "Added Attendance Data for " + today_date

        # Inserting in top level, unencrypted and hashed
        with open(total_hours_hashed_path, 'r') as total_hours_file:
            self.repo.update_file('/totalhours.csv', msg, total_hours_file.read(), self.repo.get_contents("totalhours.csv").sha, "master")

        with open(build_season_hashed_path, 'r') as build_season_file:
            self.repo.update_file('/buildseason.csv', msg, build_season_file.read(), self.repo.get_contents("buildseason.csv").sha, "master")

        with open(scans_hashed_path, 'r') as scans_hashed_file:
            self.repo.update_file('/scans.csv', msg, scans_hashed_file.read(), self.repo.get_contents("scans.csv").sha, "master")

        # Inserting in encrypted
        with open(total_hours_encrypted_path, 'r') as total_hours_encrypted_file:
            self.repo.update_file('/encrypted/totalhours.csv.gpg', msg, total_hours_encrypted_file.read(), self.repo.get_contents("encrypted/totalhours.csv.gpg").sha, "master")

        with open(build_season_encrypted_path, 'r') as build_season_encrypted_file:
            self.repo.update_file('/encrypted/buildseason.csv.gpg', msg, build_season_encrypted_file.read(), self.repo.get_contents("encrypted/buildseason.csv.gpg").sha, "master")

        with open(scans_encrypted_path, 'r') as scans_encrypted_file:
            self.repo.update_file('/encrypted/scans.csv.gpg', msg, scans_encrypted_file.read(), self.repo.get_contents("encrypted/scans.csv.gpg").sha, "master")

        try:
            os.mkdir('backups')
        except:
            pass

        os.rename(self.new_scans_path, 'backups/newscans_{}.csv'.format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))

        with open(self.new_scans_path, 'w') as new_scans_file:
            new_scans_file.write("id,date,time_in,time_out\n")
