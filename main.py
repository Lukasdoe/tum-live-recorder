from pathlib import Path
from download import download
import tum_live
import json


subjects = {
    "GDB": ("2022/W/GDB", "COMB")
}

credentials = json.load(open("credentials.json", "r"))

queue = tum_live.get_subjects(
    subjects, credentials["username"], credentials["password"])

for filename, p in queue:
    if (len(p) > 0):
        videoname, playlist_url = p[0]
        download(filename +
                 "_"+videoname+"mp4", playlist_url, Path("downloads"))
