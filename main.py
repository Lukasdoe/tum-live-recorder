from pathlib import Path
from download import download
from status_update import notification_helper
from datetime import datetime
import tum_live
import json
import sys

if len(sys.argv) != 2:
    print("usage: python", sys.argv[0], "<module-slug>")
    exit(1)

subject = sys.argv[1]
credentials = json.load(open("credentials.json", "r"))

playlist_link = tum_live.get_subject(
    subject, credentials["username"], credentials["password"])

download(subject + str(datetime.now()), playlist_link, Path("rbg-downloads"))
