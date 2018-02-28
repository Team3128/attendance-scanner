import sys
from datetime import datetime as dater
import datetime
import os
import base64
import time

from proccessrecords import RecordProccess
from datacommit import DataCommit
from github import Github

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
singleUpdateScriptPath = os.path.join(script_dir, "singleupdate.py")

print("GitHub Updater")

repo_name = "2017-18-attendance-data"

year_start = "2017-09-05"
year_end = "2018-06-12"

build_start = "2018-01-05"
build_end = "2018-02-21"

dataCommiter = DataCommit()


dataCommiter.update(repo_name, year_start, year_end, build_start, build_end)
