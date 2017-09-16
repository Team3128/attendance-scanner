import sys
from datetime import datetime as dater
import datetime
import getch
import os
import base64
import csv
import time

from proccessrecords import RecordProccess
from github import Github
from github import Repository

script_dir = os.path.dirname(__file__)
today_date = str(datetime.date.today())

# HASHED, TOP-LEVEL FILE PATHS
total_hours_path = os.path.join(script_dir, "tmp_data/totalhours.csv")
build_season_hours_path = os.path.join(script_dir, "tmp_data/buildseason.csv")

# HASHED, ACHRIVED FILE PATHS
total_hours_archived_path = os.path.join(script_dir, "tmp_data/totalhours" + today_date + ".csv")
build_season_hours_archived_path = os.path.join(script_dir, "tmp_data/buildseason" + today_date + ".csv")

# TEMPORARY, UNHASHED, ENCRYPTED FILE PATHS
total_hours_unhashed_path = os.path.join(script_dir, "tmp_data/totalhours" + today_date + "private.csv")
build_season_hours_unhashed_path = os.path.join(script_dir, "tmp_data/buildseason" + today_date + "private.csv")

# UNHASHED, ENCRYPTED FILE PATHS
total_hours_encrypted_path = os.path.join(script_dir, "tmp_data/totalhours" + today_date + "private.csv.gpg")
build_season_hours_encrypted_path = os.path.join(script_dir, "tmp_data/buildseason" + today_date + "private.csv.gpg")

# SCANS FILES
scans_hashed_path = os.path.join(script_dir, "tmp_data/scans.csv")
scans_unhashed_path = os.path.join(script_dir, "tmp_data/priv/scans.csv")
scans_encrypted_path = os.path.join(script_dir, "tmp_data/priv/scans.csv.gpg")

newscans_hashed_path = os.path.join(script_dir, "newscans.csv")

# CONFIG FILE PATHS
private_key_path = os.path.join(script_dir, "config/privatekey.txt")
gpg_pass_path = os.path.join(script_dir, "config/gpgpassphrase.txt")

g = Github()
repo = Repository()

repo_name = ""

year_start = ""
year_end = ""

build_start = ""
build_end = ""

class DataCommit:
    def __init__(self, rn, ys, ye, bs, be):
        with open(private_key_path, 'r') as privateKey:
            g = Github(privateKey.read())

        for r in g.get_user().get_repos():
            if r.name == repo_name:
                repo = r

        repo_name = rn

        year_start = ys
        year_end = ye

        build_start = bs
        build_end = be


    def update(self):
        if repo.name == repo_name:
            with open(scans_encrypted_path, 'w') as scansEnc:
                scansEnc.write(repo.get_file_contents('/private/scans.csv.gpg').decoded_content)

                os.system("gpg --passphrase-fd 0 < " + gpg_pass_path + " -o " + scans_unhashed_path + " -d " + scans_encrypted_path)

            with open(scans_unhashed_path, 'a') as scans:
                with open(newscans_hashed_path, 'r') as newScans:
                    reader = csv.DictReader(newScans, fieldnames = ['id', 'timein', 'timeout'])

                    for row in reader:
                        if row['id'] != 'id' and len(row['id']) > 4:
                            scans.write(row['id'] + ',' + row['timein'] + ',' + row['timeout'] + '\n')

            with open(newscans_hashed_path, 'w') as newScans:
                newScans.write("id,timein,timeout\n")
            os.remove(scans_encrypted_path)


            recordproccessor = RecordProccess()

            recordproccessor.proccessData(total_hours_path, year_start, year_end, True)
            recordproccessor.proccessData(build_season_hours_path, build_start, build_end, True)

            recordproccessor.proccessData(total_hours_archived_path, year_start, year_end, True)
            recordproccessor.proccessData(build_season_hours_archived_path, build_start, build_end, True)

            recordproccessor.proccessData(total_hours_unhashed_path, year_start, year_end, False)
            recordproccessor.proccessData(build_season_hours_unhashed_path, build_start, build_end, False)

            with open(scans_unhashed_path, 'r') as scansUnhashed:
                reader = csv.DictReader(scansUnhashed, fieldnames = ['id', 'timein', 'timeout'])

                with open(scans_hashed_path, 'w') as scans:
                    for row in reader:
                        scans.write(row['id'][-4:] + ',' + row['timein'] + ',' + row['timeout'] + '\n')

            # Goes to total_hours_encrypted_path
            os.system("gpg -e -r 'Team 3128' " + total_hours_unhashed_path)

            # Goes to build_season_hours_encrypted_path
            os.system("gpg -e -r 'Team 3128' " + build_season_hours_unhashed_path)

            # Goes to scans_encrypted_path
            os.system("gpg -e -r 'Team 3128' " + scans_unhashed_path)

            msg = "Added Attendance Data for " + today_date

            # Inserting in top level, unencrypted and hashed
            with open(total_hours_path, 'r') as totalFile:
                repo.update_file('/totalhours.csv', msg, totalFile.read(), repo.get_contents("totalhours.csv").sha, "master")

            with open(build_season_hours_path, 'r') as buildSeasonFile:
                repo.update_file('/buildseason.csv', msg, buildSeasonFile.read(), repo.get_contents("buildseason.csv").sha, "master")

            with open(scans_hashed_path, 'r') as scansfile:
                repo.update_file('/scans.csv', msg, scansfile.read(), repo.get_contents("scans.csv").sha, "master")

            # Inserting in 'archives' directory, unencrypted and hashed
            with open(total_hours_archived_path, 'r') as totalArchFile:
                repo.create_file('/archives/totalhours' + today_date + ".csv", msg, totalArchFile.read(), "master")

            with open(build_season_hours_archived_path, 'r') as buildSeasonArchFile:
                repo.create_file('/archives/buildseason' + today_date + ".csv", msg, buildSeasonArchFile.read(), "master")

            # Inserting in 'private' directory, encrypted
            with open(total_hours_encrypted_path, 'r') as totalArchFileEnc:
                repo.create_file('/private/totalhours' + today_date + '.csv.gpg', msg, totalArchFileEnc.read(), "master")

            with open(build_season_hours_encrypted_path, 'r') as buildSeasonArchFileEnc:
                repo.create_file('/private/buildseason' + today_date + '.csv.gpg', msg, buildSeasonArchFileEnc.read(), "master")

            with open(scans_encrypted_path, 'r') as scansFileEnc:
                repo.update_file('/private/scans.csv.gpg', msg, scansFileEnc.read(), repo.get_contents("/private/scans.csv.gpg").sha, "master")

            os.remove(total_hours_path)
            os.remove(build_season_hours_path)

            os.remove(total_hours_archived_path)
            os.remove(build_season_hours_archived_path)

            os.remove(total_hours_unhashed_path)
            os.remove(build_season_hours_unhashed_path)

            os.remove(total_hours_encrypted_path)
            os.remove(build_season_hours_encrypted_path)

            os.remove(scans_hashed_path)
            os.remove(scans_unhashed_path)
            os.remove(scans_encrypted_path)
