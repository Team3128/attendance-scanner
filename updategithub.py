import sys
import datetime
import getch
import os
import base64
import csv

from proccessrecords import RecordProccess
from github import Github

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

todayDateStr = str(datetime.date.today())

# TEMP FILE PATHS
totalFilePath = os.path.join(script_dir, "tmp_data/totalhours.csv")
buildSeasonFilePath = os.path.join(script_dir, "tmp_data/buildseason.csv")
totalArchFilePath = os.path.join(script_dir, "tmp_data/totalhours" + todayDateStr + ".csv")
buildSeasonArchFilePath = os.path.join(script_dir, "tmp_data/buildseason" + todayDateStr + ".csv")
totalFilePathPrivate = os.path.join(script_dir, "tmp_data/totalhours" + todayDateStr + "private.csv")
buildSeasonFilePathPrivate = os.path.join(script_dir, "tmp_data/buildseason" + todayDateStr + "private.csv")
totalFilePathEncrypted = os.path.join(script_dir, "tmp_data/totalhours" + todayDateStr + "private.csv.gpg")
buildSeasonFilePathEncrypted = os.path.join(script_dir, "tmp_data/buildseason" + todayDateStr + "private.csv.gpg")
scansFileOrigPathPrivate = os.path.join(script_dir, "scans.csv")
scansFilePathPrivate = os.path.join(script_dir, "tmp_data/priv/scans.csv")
scansFilePath = os.path.join(script_dir, "tmp_data/scans.csv")
scanFilePathEncrypted = os.path.join(script_dir, "tmp_data/priv/scans.csv.gpg")

# PERMANENT FILE PATHS
privateKeyPath = os.path.join(script_dir, "/config/privatekey.txt")


recordproccessor = RecordProccess()

recordproccessor.proccessData(totalFilePath, "2016-01-01", "2018-01-01", True)
recordproccessor.proccessData(buildSeasonFilePath, "2017-01-01", "2017-02-22", True)

recordproccessor.proccessData(totalArchFilePath, "2016-01-01", "2018-01-01", True)
recordproccessor.proccessData(buildSeasonArchFilePath, "2017-01-07", "2017-02-22", True)

recordproccessor.proccessData(totalFilePathPrivate, "2016-01-01", "2018-01-01", False)
recordproccessor.proccessData(buildSeasonFilePathPrivate, "2017-01-07", "2017-02-22", False)

with open(scansFileOrigPathPrivate, 'r') as scanPriv:
    reader = csv.DictReader(scanPriv, fieldnames = ['id', 'timein', 'timeout'])

    with open(scansFilePath, 'w') as scans:
        for row in reader:
            scans.write(row['id'][-4:])
            scans.write(',')
            scans.write(row['timein'])
            scans.write(',')
            scans.write(row['timeout'])
            scans.write('\n')


os.system("cp " + scansFileOrigPathPrivate + " " + scansFilePathPrivate)

os.system("gpg -e -r 'Team 3128' " + totalFilePathPrivate)
os.system("gpg -e -r 'Team 3128' " + buildSeasonFilePathPrivate)
os.system("gpg -e -r 'Team 3128' " + scansFilePathPrivate)

g = ""

with open(privateKeyPath, 'r') as privateKeyFile:
    g = Github(privateKeyFile.read())

for repo in g.get_user().get_repos():
    if repo.name == "2016-17-attendance-data":
        msg = "Added Attendance Data for " + str(datetime.date.today())
        shaStr = repo.get_git_refs()[0].object.sha

        # MARK - Inserting in top level, unencrypted and hashed

        with open(totalFilePath, 'r') as totalFile:
            repo.update_file('/totalhours.csv', msg, totalFile.read(), repo.get_contents("totalhours.csv").sha, "master")

        with open(buildSeasonFilePath, 'r') as buildSeasonFile:
            repo.update_file('/buildseason.csv', msg, buildSeasonFile.read(), repo.get_contents("buildseason.csv").sha, "master")

        with open(scansFilePath, 'r') as scansfile:
            repo.update_file('/scans.csv', msg, scansfile.read(), repo.get_contents("scans.csv").sha, "master")

         # MARK - Inserting in 'archives' directory, unencrypted and hashed

        with open(totalArchFilePath, 'r') as totalArchFile:
            repo.create_file('/archives/totalhours' + todayDateStr + ".csv", msg, totalArchFile.read(), "master")

        with open(buildSeasonArchFilePath, 'r') as buildSeasonArchFile:
            repo.create_file('/archives/buildseason' + todayDateStr + ".csv", msg, buildSeasonArchFile.read(), "master")

        # MARK - Inserting in 'private' directory, encrypted

        with open(totalFilePathEncrypted, 'r') as totalArchFileEnc:
            repo.create_file('/private/totalhours' + todayDateStr + '.csv.gpg', msg, totalArchFileEnc.read(), "master")

        with open(buildSeasonFilePathEncrypted, 'r') as buildSeasonArchFileEnc:
            repo.create_file('/private/buildseason' + todayDateStr + '.csv.gpg', msg, buildSeasonArchFileEnc.read(), "master")

        with open(scanFilePathEncrypted, 'r') as scansFileEnc:
            repo.update_file('/private/scans.csv.gpg', msg, scansFileEnc.read(), repo.get_contents("/private/scans.csv.gpg").sha, "master")

os.remove(totalFilePath)
os.remove(buildSeasonFilePath)
os.remove(totalArchFilePath)
os.remove(buildSeasonArchFilePath)
os.remove(totalFilePathPrivate)
os.remove(buildSeasonFilePathPrivate)
os.remove(totalFilePathEncrypted)
os.remove(buildSeasonFilePathEncrypted)
os.remove(scansFileOrigPathPrivate)
os.remove(scansFilePathPrivate)
os.remove(scansFilePath)
os.remove(scanFilePathEncrypted)
