import requests


def notification_helper(notifcationURL, username, message):

    print("Sending notification to "+notifcationURL)

    requests.post(notifcationURL, data={
        "username": username,
        "message": message
    })
