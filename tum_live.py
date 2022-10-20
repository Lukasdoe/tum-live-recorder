import argparse
import os
import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# From
# https://github.com/Valentin-Metz/tum_video_scraper


def enumerate_list(list_of_tuples):
    return [(f'{index:03d}_{name}', url) for index, (name, url) in enumerate(list_of_tuples)]


def login(tum_username: str, tum_password: str) -> webdriver:

    driver = webdriver.Chrome("/usr/bin/chromedriver")

    print("Logging in..")
    driver.get("https://live.rbg.tum.de/login")
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div/div/button").click()
    driver.find_element(By.ID, "username").send_keys(tum_username)
    driver.find_element(By.ID, "password").send_keys(tum_password)
    driver.find_element(By.ID, "username").submit()
    sleep(2)
    if "Couldn't log in. Please double check your credentials." in driver.page_source:
        driver.close()
        raise argparse.ArgumentTypeError("Username or password incorrect")
    return driver


def get_video_links_of_subject(driver: webdriver, subjects_identifier, camera_type):
    subject_url = "https://live.rbg.tum.de/course/" + subjects_identifier
    driver.get(subject_url)

    links_on_page = driver.find_elements(By.XPATH, ".//a")
    video_urls = []
    for link in links_on_page:
        link_url = link.get_attribute("href")
        if link_url and "https://live.rbg.tum.de/w/" in link_url:
            video_urls.append(link_url)

    video_urls = [url for url in video_urls if (
        "/CAM" not in url and "/PRES" not in url)]
    video_urls = list(dict.fromkeys(video_urls))  # deduplicate

    video_playlists = []
    for video_url in video_urls:
        driver.get(video_url + "/" + camera_type)
        sleep(2)
        filename = driver.find_element(
            By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[2]/div/div/i").text.strip()

        playlist_url = get_playlist_url(driver.page_source)
        video_playlists.append((filename, playlist_url))

    video_playlists.reverse()
    return video_playlists


def get_playlist_url(source: str) -> str:
    prefix = 'https://stream.lrz.de/vod/_definst_/mp4:tum/RBG/'
    postfix = '/playlist.m3u8'
    playlist_extracted_url = re.search(prefix + '(.+?)' + postfix, source)
    if not playlist_extracted_url:
        prefix = "https://live.stream.lrz.de/livetum/"
        playlist_extracted_url = re.search(prefix + '(.+?)' + postfix, source)
    if not playlist_extracted_url:
        raise Exception(
            "Could not extract playlist URL from TUM-live! Page source:\n" + source)
    playlist_extracted_url = playlist_extracted_url.group(1)
    playlist_url = prefix + playlist_extracted_url + postfix
    return playlist_url


def get_subjects(subjects, tum_username: str, tum_password: str):
    driver = login(tum_username, tum_password)
    queue=[]
    for subject_name, (subjects_identifier, camera_type) in subjects.items():
        print(
            f"Scanning video links for: {subject_name} ({subjects_identifier}) of the {camera_type}..")
        m3u8_playlists = get_video_links_of_subject(
            driver, subjects_identifier, camera_type)
        m3u8_playlists = enumerate_list(m3u8_playlists)

        print(f'Found {len(m3u8_playlists)} videos for "{subject_name}"')
        queue.append((subject_name, m3u8_playlists))
    driver.close()
    return queue
