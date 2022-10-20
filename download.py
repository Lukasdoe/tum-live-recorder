from pathlib import Path
import subprocess
import time


def download(filename: str, playlist_url: str, tmp_directory: Path):

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
