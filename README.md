# Live-RBG-Recorder
Downloads livestrams from **live.rbg.tum.de**

## Usage
This application can be used to download stored lecture recordings, but it is mainly intended to download live streams that are not recorded by https://live.rbg.tum.de/.

It works by *attending* the lecture while it is being streamed and then downloading it on the fly using ffmpeg.

## Prerequisites
In order for the script to work, you need to create a **credentials.json** file in the root folder with the following format:

```json
{
  "username": "YOUR_TUM_USERNAME (ex. ge12abc)",
  "password": "YOUR_TUM_PASSWORD"
}
```

This allows the script to log in to tum-live and extract the currently playing streams.

You can select the lectures you want to download by adjusting the desired subjects in [main.py](main.py).

The format is:

```python
{
DOWNLOAD_NAME : (TUM_LIVE_IDENTIFIER, CAMERA_VIEW)
}
```

> **_NOTE:_** You can find the corresponding `TUM_LIVE_IDENTIFIER` in the url for a given subject on tum-live.

An example configuration could look like this:

```python
{
"GDB": ("2022/W/GDB", "COMB"),
"ITSEC": ("2022/W/ItSec", "COMB")
}
```

## Automation
If you don't want to manually start the script every time a desired lecture is live, you can create a corresponding **cron-task** which starts the script at the correct time 

You can use this website to create the correct timings: [crontab.guru](https://crontab.guru/).
