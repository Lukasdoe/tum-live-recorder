import subprocess
import sys
import time
from pathlib import Path


def download_and_cut_video(filename: str, playlist_url: str, output_file_path: Path, tmp_directory: Path):

    if not tmp_directory.exists():
        tmp_directory.mkdir(parents=True)

    temporary_path = Path(tmp_directory, filename +
                          ".mp4")  # Download location

    download_start_time = time.time()  # Track download time

    print(f"Download of {filename} started")
    subprocess.run([
        'ffmpeg',
        '-y',  # Overwrite output file if it already exists
        '-hwaccel', 'auto',  # Hardware acceleration
        '-i', playlist_url,  # Input file
        '-c', 'copy',  # Codec name
        '-f', 'mp4',  # Force mp4 as output file format
        temporary_path  # Output file
    ])

    print(
        f"Download of {filename} completed after {(time.time() - download_start_time):.0f}s")
 
    print(
        f"Completed {filename} after {(time.time() - download_start_time):.0f}s")


url = "https://stream.lrz.de/vod/_definst_/mp4:tum/RBG/GBS_2022_10_19_11_00COMB.mp4/playlist.m3u8"
filename = "test"
output_file_path = Path("test.mp4")
download_directory = Path("downloads")

download_and_cut_video(filename, url, output_file_path, download_directory)
