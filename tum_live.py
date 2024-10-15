import argparse
import re
from time import sleep
import json

from selenium import webdriver
from selenium.webdriver.common.by import By

# From
# https://github.pcom/Valentin-Metz/tum_video_scraper


def enumerate_list(list_of_tuples):
    return [(f'{index:03d}', url) for index, url in enumerate(list_of_tuples)]


def login(tum_username: str, tum_password: str) -> webdriver.Chrome:
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("--headless")
    driver = webdriver.Chrome(
        "/usr/lib/chromium-browser/chromedriver", options=driver_options)

    print("Logging in..")
    driver.get("https://live.rbg.tum.de/login")
    driver.find_element(
        By.XPATH, "/html/body/main/section/article/a").click()
    # wait until all redirects have succeeded
    sleep(5)
    driver.find_element(By.ID, "username").send_keys(tum_username)
    driver.find_element(By.ID, "password").send_keys(tum_password)
    driver.find_element(By.ID, "btnLogin").click()
    sleep(2)
    if "Web Login Service" in driver.page_source:
        driver.close()
        raise argparse.ArgumentTypeError("Username or password incorrect")
    return driver


def get_video_link_of_subject(driver: webdriver.Chrome, subject):
    subject_info_url = "https://live.rbg.tum.de/api/courses/" + subject
    driver.get(subject_info_url)
    json_text = driver.find_element(By.XPATH, "/html/body/pre").text
    subject_info = json.loads(json_text)

    if "status" in subject_info and subject_info["status"] != 200:
        if "message" in subject_info:
            raise argparse.ArgumentTypeError(subject_info["message"])
        raise Exception("Error during class lookup")

    assert subject_info["Visibility"] == "loggedin"
    assert subject_info["Slug"] == subject

    if subject_info["NextLecture"]["HLSUrl"] == "":
        raise Exception("No ongoing lecture :/")

    return subject_info["NextLecture"]["HLSUrl"]


def get_subject(subject, tum_username: str, tum_password: str):
    driver = login(tum_username, tum_password)
    m3u8_playlist = get_video_link_of_subject(driver, subject)

    print(f'Found "{m3u8_playlist}" for "{subject}"')
    driver.close()
    return m3u8_playlist
