# TODO 1: ADD TYPE HINTS
# TODO 2: ADD tests for all functions


##############################################################################################
##      This Bot Will Log you to 1337.ma as soon as any tweet pushed about piscine          ##
##      To setup this bot you need first to get a twitterAPI v2 Bearer Token                ##
##      create a .credential folder                                                         ##
##      inside the .credentials/ create a json file with "credential.json" as a name        ##
##      Inside credential.json                                                              ##
##      {                                                                                   ##
##        "Bearers": "paste your twitter bearer here",                                       ##
##        "email": "email@example.com",                                                     ##
##        "password": "this is a password"                                                  ##
##      }                                                                                   ##
##############################################################################################

import json
import os
from threading import Thread
from time import sleep
import webbrowser
from itertools import cycle

import requests
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CREDS = "/home/redone/Projects/Personal/1337BOT/.credentials/credential.json"
LAST_TWEET = "/home/redone/Projects/Personal/1337BOT/last_tweet.txt"
SOUND = "/home/redone/Projects/Personal/1337BOT/assets/audio.mp3"

KEYWORDS = [
    "http://candidature.1337.ma",
    "pool",
    "open",
    "dates",
    "inscription",
    "piscine",
    "ouvert",
    "مسبح",
    "بول",
    "ترشيح",
    "بيسين",
    "choisissez",
]

BEARER_TOKENS = cycle([
    "AAAAAAAAAAAAAAAAAAAAAEk7cwEAAAAAzgm1z7Wm4HenPhbgK2s4Iw80rCY%3DS7cDnpdEAkPK5B0BqTTHZRYkMnIuzp08FpP5LnbtpD95NXmqjw",
    "AAAAAAAAAAAAAAAAAAAAACUOdAEAAAAATt0g0xv%2B%2F%2B7lpurYkGNe6N%2FTS34%3DcafYj3ayCWc9rIzusgH1N2clIUn5a1XgRDTRWfc1dmucHUg3YH",
    "AAAAAAAAAAAAAAAAAAAAAPwrdAEAAAAAOsez3OwDr57t7w0WKG9QIY1%2BR9c%3Dkp8Mh5iuP2fHrQDLcYAT0xn5RWnW1Wk6x9tdvKlbGSjI54fhKC",
])


def create_url():
    user_id = 971012509032427520
    # return "https://api.twitter.com/2/users/1527778571326038021/tweets"
    return f"https://api.twitter.com/2/users/{user_id}/tweets"


def get_params():
    return {"max_results": 5}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    global BEARER_TOKENS
    token = next(BEARER_TOKENS)
    r.headers["Authorization"] = f"Bearer {token}"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}"
        )
    return response.json()


def get_last_tweet():
    os.system("clear")
    url = create_url()
    params = get_params()
    return connect_to_endpoint(url, params)["data"][0]["text"].lower()


def is_keyword_in_last_tweet(tweet=None) -> bool:
    last_tweet = get_last_tweet()
    tweet = last_tweet if tweet is None else tweet
    return any([True if key.lower() in tweet else False for key in KEYWORDS])


def get_credentials():
    with open(CREDS, "r", encoding="utf-8") as f:
        return json.load(f)



def open_browser():
    # options = Options()
    # options.add_experimental_option("detach", True)
    # options.binary_location = "/usr/bin/brave"
    # options.add_argument("--kiosk")  # To open Brave in Full Screen
    # driver = webdriver.Chrome(options=options)
    # driver.get("https://candidature.1337.ma/users/sign_in")
    # driver.find_element(By.ID, "user_email").send_keys(get_credentials()["email"])
    # driver.find_element(By.ID, "user_password").send_keys(get_credentials()["password"])
    # WebDriverWait(driver, 5).until(
    #     EC.element_to_be_clickable(
    #         (
    #             By.CSS_SELECTOR,
    #             "div a.cc-btn.cc-allow",
    #         )
    #     )
    # ).click()
    # driver.find_element(By.XPATH, '//*[@id="new_user"]/div[2]/div[3]/input').click()
    # scroll_to_buttom = "window.scrollTo(0, document.documentElement.scrollHeight)"
    # driver.execute_script(scroll_to_buttom)
    webbrowser.open("https://candidature.1337.ma/users/sign_in")
    

def alert_sound():
    os.system("pactl set-sink-volume 0 +500%")
    [playsound(SOUND) for _ in range(10)]


def alert_script():
    [print("\033[91mGO GO GOOOO GO GO GOOOO!!\033[00m") for _ in range(10)]


def trigger_alert():
    alert_script()
    Thread(target=open_browser).start()
    Thread(target=alert_sound).start()


def keep_searching():
    sleep(10)
    os.system("clear")


def main():
    os.system("clear")
    while True:
        if is_keyword_in_last_tweet():
            trigger_alert()
            break
        else:
            print("Nothing Found Yet!")
            keep_searching()


if __name__ == "__main__":
    main()




