from pathlib import Path
from download import download
import tum_live
import json


subjects = {
    "GDB": ("2022/W/GDB", "COMB"),
}

credentials = json.load(open("/home/pi/live-rbg-recorder/credentials.json", "r"))

queue = tum_live.get_subjects(
    subjects, credentials["username"], credentials["password"])

for filename, p in queue:
    for videoname,playlist_url in p:
        download(filename +
                 "_"+videoname+"mp4", playlist_url, Path("rbg-downloads"))
