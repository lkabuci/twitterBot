from pathlib import Path
import requests

from main import (
    alert_sound,
    alert_script,
    trigger_alert,
    get_credentials,
    check_last_tweet,
    open_browser,
    CREDS,
    SOUND,
    KEYWORDS,
)


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
        "Authorization": f"Bearer {get_credentials()['Bearer']}",
    }
    response = requests.get(url, headers=headers).status_code
    assert response == 200
