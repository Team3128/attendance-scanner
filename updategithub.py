from github import Github
import sys
import datetime
import getch
import os
import base64
import csv

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

totalFileRelPath = "tmp_data/totalhours.csv"
totalFileAbsPath = os.path.join(script_dir, totalFileRelPath)

buildSeasonFileRelPath = "tmp_data/buildseason.csv"
buildSeasonFileAbsPath = os.path.join(script_dir, buildSeasonFileRelPath)

totalArchFileRelPath = "tmp_data/totalhours" + str(datetime.date.today()) + ".csv"
totalArchFileAbsPath = os.path.join(script_dir, totalArchFileRelPath)

buildSeasonArchFileRelPath = "tmp_data/buildseason" + str(datetime.date.today()) + ".csv"
buildSeasonArchFileAbsPath = os.path.join(script_dir, buildSeasonArchFileRelPath)

totalFileRelPathPrivate = "tmp_data/totalhours" + str(datetime.date.today()) + "private.csv"
totalFileAbsPathPrivate = os.path.join(script_dir, totalFileRelPathPrivate)

buildSeasonFileRelPathPrivate = "tmp_data/buildseason" + str(datetime.date.today()) + "private.csv"
buildSeasonFileAbsPathPrivate = os.path.join(script_dir, buildSeasonFileRelPathPrivate)

totalFileRelPathEncrypted = "tmp_data/totalhours" + str(datetime.date.today()) + "private.csv.gpg"
totalFileAbsPathEncrypted = os.path.join(script_dir, totalFileRelPathEncrypted)

buildSeasonFileRelPathEncrypted = "tmp_data/buildseason" + str(datetime.date.today()) + "private.csv.gpg"
buildSeasonFileAbsPathEncrypted = os.path.join(script_dir, buildSeasonFileRelPathEncrypted)

scansFileOrigRelPathPrivate = "scans.csv"
scansFileOrigAbsPathPrivate = os.path.join(script_dir, scansFileOrigRelPathPrivate)

scansFileRelPathPrivate = "tmp_data/priv/scans.csv"
scansFileAbsPathPrivate = os.path.join(script_dir, scansFileRelPathPrivate)

scansFileRelPath = "tmp_data/scans.csv"
scansFileAbsPath = os.path.join(script_dir, scansFileRelPath)

scanFileRelPathEncrypted = "tmp_data/priv/scans.csv.gpg"
scanFileAbsPathEncrypted = os.path.join(script_dir, scanFileRelPathEncrypted)

privateKeyPath = os.path.join(script_dir, "/config/privatekey.txt")


os.system("python " + os.path.join(script_dir, "proccessrecords.py") + " " + totalFileAbsPath + " 2016-01-01 " + " hash=true")
os.system("python " + os.path.join(script_dir, "proccessrecords.py") + " " + buildSeasonFileAbsPath + " 2017-01-07 " + " hash=true")

os.system("python " + os.path.join(script_dir, "proccessrecords.py") + " " + totalArchFileAbsPath + " 2016-01-01 " + " hash=true")
os.system("python " + os.path.join(script_dir, "proccessrecords.py") + " " + buildSeasonArchFileAbsPath + " 2017-01-07 " + " hash=true")

os.system("python " + os.path.join(script_dir, "proccessrecords.py") + " " + totalFileAbsPathPrivate + " 2016-01-01 " + " hash=false")
os.system("python " + os.path.join(script_dir, "proccessrecords.py") + " " + buildSeasonFileAbsPathPrivate + " 2017-01-07 " + " hash=false")

with open(scansFileOrigAbsPathPrivate, 'r') as scanPriv:
    reader = csv.DictReader(scanPriv, fieldnames = ['id', 'timein', 'timeout'])

    with open(scansFileAbsPath, 'w') as scans:
        for row in reader:
            scans.write(row['id'][-4:])
            scans.write(',')
            scans.write(row['timein'])
            scans.write(',')
            scans.write(row['timeout'])
            scans.write('\n')
os.system("cp " + scansFileOrigAbsPathPrivate + " " + scansFileAbsPathPrivate)

os.system("gpg -e -r 'Team 3128' " + totalFileAbsPathPrivate)
os.system("gpg -e -r 'Team 3128' " + buildSeasonFileAbsPathPrivate)
os.system("gpg -e -r 'Team 3128' " + scansFileAbsPathPrivate)

g = ""

with open(privateKeyPath, 'r') as privateKeyFile:
    g = Github(privateKeyFile.read())

for repo in g.get_user().get_repos():
    if repo.name == "2016-17-attendance-data":
        msg = "Added Attendance Data for " + str(datetime.date.today())
        shaStr = repo.get_git_refs()[0].object.sha

        # MARK - Inserting in top level, unencrypted and hashed

        with open(totalFileAbsPath, 'r') as totalFile:
            repo.update_file('/totalhours.csv', msg, totalFile.read(), repo.get_contents("totalhours.csv").sha, "master")

        with open(buildSeasonFileAbsPath, 'r') as buildSeasonFile:
            repo.update_file('/buildseason.csv', msg, buildSeasonFile.read(), repo.get_contents("buildseason.csv").sha, "master")

        with open(scansFileAbsPath, 'r') as scansfile:
            repo.update_file('/scans.csv', msg, scansfile.read(), repo.get_contents("scans.csv").sha, "master")

         # MARK - Inserting in 'archives' directory, unencrypted and hashed

        with open(totalArchFileAbsPath, 'r') as totalArchFile:
            repo.create_file('/archives/totalhours' + str(datetime.date.today()) + ".csv", msg, totalArchFile.read(), "master")

        with open(buildSeasonArchFileAbsPath, 'r') as buildSeasonArchFile:
            repo.create_file('/archives/buildseason' + str(datetime.date.today()) + ".csv", msg, buildSeasonArchFile.read(), "master")

        # MARK - Inserting in 'private' directory, encrypted

        with open(totalFileAbsPathEncrypted, 'r') as totalArchFileEnc:
            repo.create_file('/private/totalhours' + str(datetime.date.today()) + '.csv.gpg', msg, totalArchFileEnc.read(), "master")

        with open(buildSeasonFileAbsPathEncrypted, 'r') as buildSeasonArchFileEnc:
            repo.create_file('/private/buildseason' + str(datetime.date.today()) + '.csv.gpg', msg, buildSeasonArchFileEnc.read(), "master")

        with open(scanFileAbsPathEncrypted, 'r') as scansFileEnc:
            repo.update_file('/private/scans.csv.gpg', msg, scansFileEnc.read(), repo.get_contents("/private/scans.csv.gpg").sha, "master")

os.remove(scansFileAbsPath)
os.remove(totalFileAbsPath)
os.remove(buildSeasonFileAbsPath)
os.remove(totalArchFileAbsPath)
os.remove(buildSeasonArchFileAbsPath)
os.remove(totalFileAbsPathPrivate)
os.remove(buildSeasonFileAbsPathPrivate)
os.remove(totalFileAbsPathEncrypted)
os.remove(scanFileAbsPathEncrypted)
os.remove(scansFileAbsPathPrivate)
os.remove(buildSeasonFileAbsPathEncrypted)


