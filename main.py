##############################################################################################
##      Author: {                                                                           ##
##          redouane elkaboussi                                                             ##
##          twitter: @kaboussi_                                                             ##
##          github: @kaboussi                                                               ##
##      }                                                                                   ##
##############################################################################################
from tokens import tokens

import json
import os
from itertools import cycle
from threading import Thread
from time import sleep

import requests
from playsound import playsound

SOUND = "./assets/audio.mp3"

# here you need to define a keywords that may be interesting in the new tweet
KEYWORDS = [
    "Key 1",
    "Key 2",
    "Key 3",
    "Key 4",
    "Key 5",
    "Key 6",
    "Key 7",
    "..."
]

BEARER_TOKENS = cycle(tokens)


def create_url():
    # define the target twittwer user ID 
    user_id: int = 0
    return f"https://api.twitter.com/2/users/{user_id}/tweets"


def get_params():
    # i set it up to the last 5 tweets to not waste the number of requests
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


def get_last_tweet() -> str:
    """return the last tweet as a string"""
    os.system("clear")
    url = create_url()
    params = get_params()
    return connect_to_endpoint(url, params)["data"][0]["text"].lower()


def is_keyword_in_last_tweet(tweet=None) -> bool:
    last_tweet = get_last_tweet()
    tweet = last_tweet if tweet is None else tweet
    return any([True if key.lower() in tweet else False for key in KEYWORDS])


def you_next_step():
    # define what you want to do if a tweet matches the requirements
    pass


def alert_sound():
    # trigger sound allert if a tweet matches the requirements
    os.system("pactl set-sink-volume 0 +500%")
    [playsound(SOUND) for _ in range(10)]


def alert_script():
    [print("\033[91mGO GO GOOOO GO GO GOOOO!!\033[00m") for _ in range(10)]


def trigger_alert():
    alert_script()
    Thread(target=you_next_step).start()
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
