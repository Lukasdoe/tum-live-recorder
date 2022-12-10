from pathlib import Path
from download import download
import tum_live
import json
from status_update import notification_helper

subjects = {
    "GDB": ("2022/W/GDB", "COMB"),
}

credentials = json.load(
    open("/home/pi/live-rbg-recorder/credentials.json", "r"))

try:
    queue = tum_live.get_subjects(
        subjects, credentials["username"], credentials["password"])
    for filename, p in queue:
        for videoname, playlist_url in p:

            notification_helper(
                credentials["notificationURL"], credentials["senderEmail"], "RBG-Recorder started downloading:\n"+videoname)

            download(filename +
                     "_"+videoname+"mp4", playlist_url, Path("rbg-downloads"))

except Exception as e:
    message = "RBG-Recorder failed with error:\n"+str(e)

    notification_helper(
        credentials["notificationURL"], credentials["senderEmail"], message)
