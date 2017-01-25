import sys
import datetime
import getch
import os
import base64
import csv

from proccessrecords import RecordProccess
from github import Github
from lcdpanel import LCDPanel
lcd = LCDPanel(0.0)

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

todayDateStr = str(datetime.date.today())

# HASHED, TOP-LEVEL FILE PATHS
totalHoursPath = os.path.join(script_dir, "tmp_data/totalhours.csv")
buildSeasonHoursPath = os.path.join(script_dir, "tmp_data/buildseason.csv")

# HASHED, ACHRIVED FILE PATHS
totalHoursArchivedPath = os.path.join(script_dir, "tmp_data/totalhours" + todayDateStr + ".csv")
buildSeasonHoursArchivedPath = os.path.join(script_dir, "tmp_data/buildseason" + todayDateStr + ".csv")

# TEMPORARY, UNHASHED, ENCRYPTED FILE PATHS
totalHoursUnhashedPath = os.path.join(script_dir, "tmp_data/totalhours" + todayDateStr + "private.csv")
buildSeasonHoursUnhashedPath = os.path.join(script_dir, "tmp_data/buildseason" + todayDateStr + "private.csv")

# UNHASHED, ENCRYPTED FILE PATHS
totalHoursEncryptedPath = os.path.join(script_dir, "tmp_data/totalhours" + todayDateStr + "private.csv.gpg")
buildSeasonHoursEncryptedPath = os.path.join(script_dir, "tmp_data/buildseason" + todayDateStr + "private.csv.gpg")

# SCANS FILES
scansPath = os.path.join(script_dir, "tmp_data/scans.csv")
scansUnhashedPath = os.path.join(script_dir, "tmp_data/priv/scans.csv")
scansEncryptedPath = os.path.join(script_dir, "tmp_data/priv/scans.csv.gpg")

newScansPath = os.path.join(script_dir, "newscans.csv")

# CONFIG FILE PATHS
privateKeyPath = os.path.join(script_dir, "config/privatekey.txt")
gpgPassPath = os.path.join(script_dir, "config/gpgpassphrase.txt")

lcd.display("Uploading...\nDo not scan.")

g = Github()
with open(privateKeyPath, 'r') as privateKey:
    g = Github(privateKey.read())

for repo in g.get_user().get_repos():
    if repo.name == "2016-17-attendance-data":
        with open(scansEncryptedPath, 'w') as scansEnc:
            scansEnc.write(repo.get_file_contents('/private/scans.csv.gpg').decoded_content)

        os.system("gpg --passphrase-fd 0 < " + gpgPassPath + " -o " + scansUnhashedPath + " -d " + scansEncryptedPath)

        with open(scansUnhashedPath, 'a') as scans:
            with open(newScansPath, 'r') as newScans:
                reader = csv.DictReader(newScans, fieldnames = ['id', 'timein', 'timeout'])

                for row in reader:
                    if row['id'] != 'id' and len(row['id']) > 4:
                        scans.write(row['id'] + ',' + row['timein'] + ',' + row['timeout'] + '\n')

        with open(newScansPath, 'w') as newScans:
            newScans.write("id,timein,timeout\n")
        os.remove(scansEncryptedPath)


recordproccessor = RecordProccess()

recordproccessor.proccessData(totalHoursPath, "2016-01-01", "2018-01-01", True)
recordproccessor.proccessData(buildSeasonHoursPath, "2017-01-01", "2017-02-22", True)

recordproccessor.proccessData(totalHoursArchivedPath, "2016-01-01", "2018-01-01", True)
recordproccessor.proccessData(buildSeasonHoursArchivedPath, "2017-01-07", "2017-02-22", True)

recordproccessor.proccessData(totalHoursUnhashedPath, "2016-01-01", "2018-01-01", False)
recordproccessor.proccessData(buildSeasonHoursUnhashedPath, "2017-01-07", "2017-02-22", False)

with open(scansUnhashedPath, 'r') as scansUnhashed:
    reader = csv.DictReader(scansUnhashed, fieldnames = ['id', 'timein', 'timeout'])

    with open(scansPath, 'w') as scans:
        for row in reader:
            scans.write(row['id'][-4:] + ',' + row['timein'] + ',' + row['timeout'] + '\n')

os.system("gpg -e -r 'Team 3128' " + totalHoursUnhashedPath)
os.system("gpg -e -r 'Team 3128' " + buildSeasonHoursUnhashedPath)
os.system("gpg -e -r 'Team 3128' " + scansUnhashedPath)

for repo in g.get_user().get_repos():
    if repo.name == "2016-17-attendance-data":
        msg = "Added Attendance Data for " + str(datetime.date.today())

        # Inserting in top level, unencrypted and hashed

        with open(totalHoursPath, 'r') as totalFile:
            repo.update_file('/totalhours.csv', msg, totalFile.read(), repo.get_contents("totalhours.csv").sha, "master")

        with open(buildSeasonHoursPath, 'r') as buildSeasonFile:
            repo.update_file('/buildseason.csv', msg, buildSeasonFile.read(), repo.get_contents("buildseason.csv").sha, "master")

        with open(scansPath, 'r') as scansfile:
            repo.update_file('/scans.csv', msg, scansfile.read(), repo.get_contents("scans.csv").sha, "master")

         # Inserting in 'archives' directory, unencrypted and hashed

        with open(totalHoursArchivedPath, 'r') as totalArchFile:
            repo.create_file('/archives/totalhours' + todayDateStr + ".csv", msg, totalArchFile.read(), "master")

        with open(buildSeasonHoursArchivedPath, 'r') as buildSeasonArchFile:
            repo.create_file('/archives/buildseason' + todayDateStr + ".csv", msg, buildSeasonArchFile.read(), "master")

        # Inserting in 'private' directory, encrypted

        with open(totalHoursEncryptedPath, 'r') as totalArchFileEnc:
            repo.create_file('/private/totalhours' + todayDateStr + '.csv.gpg', msg, totalArchFileEnc.read(), "master")

        with open(buildSeasonHoursEncryptedPath, 'r') as buildSeasonArchFileEnc:
            repo.create_file('/private/buildseason' + todayDateStr + '.csv.gpg', msg, buildSeasonArchFileEnc.read(), "master")

        with open(scansEncryptedPath, 'r') as scansFileEnc:
            repo.update_file('/private/scans.csv.gpg', msg, scansFileEnc.read(), repo.get_contents("/private/scans.csv.gpg").sha, "master")

os.remove(totalHoursPath)
os.remove(buildSeasonHoursPath)

os.remove(totalHoursArchivedPath)
os.remove(buildSeasonHoursArchivedPath)

os.remove(totalHoursUnhashedPath)
os.remove(buildSeasonHoursUnhashedPath)

os.remove(totalHoursEncryptedPath)
os.remove(buildSeasonHoursEncryptedPath)

os.remove(scansPath)
os.remove(scansUnhashedPath)
os.remove(scansEncryptedPath)

lcd.clear_screen()
