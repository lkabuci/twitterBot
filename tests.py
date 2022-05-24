from pathlib import Path

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from main import CREDS, SOUND, get_all_tweets, get_credentials, is_keyword_in_last_tweet


def test_sound_file_exists():
    path = Path(SOUND)
    assert path.is_file() and path.exists()


def test_creds_file_exists():
    path = Path(CREDS)
    assert path.is_file() and path.exists()


def test_request_api():
    url = "https://api.twitter.com/2/tweets/search/recent?query=from:1337FIL"
    bearer = get_credentials()["Bearer"]
    headers = {
        "Authorization": f"Bearer {bearer}",
    }
    response = requests.get(url, headers=headers).status_code
    assert response == 200


def test_get_all_tweets():
    # If "meta" is in json response means that is valid
    assert "meta" in get_all_tweets()


def test_is_keyword_in_last_tweet():
    false_tweet = "This tweet doesn't contain any of the speacial Keywords"
    right_tweet = "This tweet contain a special Pool keyword"
    arabic_tweet = "Test the arabic language المسبح"

    assert is_keyword_in_last_tweet(false_tweet) == False
    assert is_keyword_in_last_tweet(right_tweet) == True
    assert is_keyword_in_last_tweet(arabic_tweet) == True


def test_selenium():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/brave"
    chrome_options.add_argument("--headless")  # To open in background
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.1337.ma/")

    assert "1337 Coding School" == driver.title
