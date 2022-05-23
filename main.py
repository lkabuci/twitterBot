##############################################################################################
##      To setup this bot you need first to get a twitterAPI v2 Bearer Token                ##
##      create a .credential folder                                                         ##
##      inside the .credentials/ create a json file with "credential.json" as a name        ##
##      Inside credential.json                                                              ##
##      {                                                                                   ##
##        "Bearer": "paste your twitter bearer here",                                       ##
##        "email": "email@example.com",                                                     ##
##        "password": "this is a password"                                                  ##
##      }                                                                                   ##
##############################################################################################

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import json
from time import sleep
from threading import Thread

import requests
from playsound import playsound

CREDS = "/home/redone/Projects/Personal/1337BOT/.credentials/credential.json"
LAST_TWEET = "/home/redone/Projects/Personal/1337BOT/last_tweet.txt"

def get_credentials():
    with open(CREDS, "r", encoding="utf-8") as f:
        return json.load(f)


def check_last_tweet():
    # testing!
    # url = "https://api.twitter.com/2/tweets/search/recent?query=from:underm18"
    url = 'https://api.twitter.com/2/tweets/search/recent?query=from:1337FIL'
    headers = {
        "Authorization": f"Bearer {get_credentials()['Bearer']}",
    }
    try:
        response = requests.get(url, headers=headers).json()
    except ConnectionError:
        sleep(300)
        check_last_tweet()
    else:
        last_tweet = response["data"][0]["text"].lower()
        last_tweet_id = response["data"][0]["id"]
        with open(LAST_TWEET) as f: last_stored_tweet = f.readline().strip()
        if last_stored_tweet != last_tweet_id:
            print(last_tweet)
            return True
        return False


def open_browser():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.binary_location = "/usr/bin/brave"
    chrome_options.add_argument("--kiosk") # To open Brave in Full Screen
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://candidature.1337.ma/users/sign_in")
    driver.find_element(By.ID, "user_email").send_keys(get_credentials()["email"])
    driver.find_element(By.ID, "user_password").send_keys(get_credentials()["password"])
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "body > div.cc-window.cc-floating.cc-type-opt-in.cc-theme-block.cc-bottom.cc-right.cc-color-override--390765418 > div > a.cc-btn.cc-allow",
            )
        )
    ).click()
    
    driver.find_element(By.XPATH, '//*[@id="new_user"]/div[2]/div[3]/input').click()

def alert_sound():
    os.system("pactl set-sink-volume 0 +500%")
    [playsound("./assets/audio.mp3") for _ in range(10)]


def alert_script():
    [print("\033[91mGO GO GOOOO GO GO GOOOO!!\033[00m") for _ in range(10)]


def trigger_alert():
    Thread(target=open_browser).start()
    Thread(target=alert_sound).start()
    Thread(target=alert_script).start()


def keep_searching():
    sleep(10)
    os.system("clear")


def main():
    os.system("clear")
    while True:
        if check_last_tweet():
            trigger_alert()
            break
        else:
            print("Nothing Found Yet!")
            keep_searching()


if __name__ == "__main__":
    main()
    