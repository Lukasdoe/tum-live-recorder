from pathlib import Path
from download import download
import tum_live
import json
from status_update import notification_helper

subjects = {
    "GDB": ("2022/W/GDB", "COMB")
}

credentials = json.load(open("credentials.json", "r"))

try:
    subjects = tum_live.get_subjects(
        subjects, credentials["username"], credentials["password"])

    for subject_name, video_queue in subjects:
        for videoname, playlist_url in video_queue:

            notification_helper(
                credentials["notificationURL"], credentials["senderEmail"], "RBG-Recorder started downloading:\n"+videoname)

            download(subject_name + "_" + videoname,
                     playlist_url, Path("rbg-downloads"))

except Exception as e:
    message = "RBG-Recorder failed with error:\n"+str(e)

    notification_helper(
        credentials["notificationURL"], credentials["senderEmail"], message)
