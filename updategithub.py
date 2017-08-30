import sys
from datetime import datetime as dater
import datetime
import os
import base64
import time

from proccessrecords import RecordProccess
from github import Github

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
singleUpdateScriptPath = os.path.join(script_dir, "singleupdate.py")

lastFilePath = os.path.join(script_dir, "last.txt")
with open(lastFilePath, 'w') as lastfile:
    lastfile.write("NOT")
print("GitHub Updater")

inittime = dater.strptime(str(dater.today()), '%Y-%m-%d %H:%M:%S.%f')

while True:
    nowtime = dater.strptime(str(dater.today()), '%Y-%m-%d %H:%M:%S.%f')

    if nowtime.date() != inittime.date() :
        inittime = dater.strptime(str(dater.today()), '%Y-%m-%d %H:%M:%S.%f')

        os.system("python " + singleUpdateScriptPath)
        
    time.sleep(30)
