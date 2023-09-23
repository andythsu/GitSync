from time import sleep
from urllib.parse import parse_qs
import requests
from logger import set_logging, debug, info

client_id = "5fbc80938f0fa9cebefa"
client_secret = "bbec7dfe54df734011ece4d35f0ff4c510afad4b"

set_logging()

def get_access_token():
    auth_url = "https://github.com/login/device/code?scope=repo"
    auth_url_res = requests.post(auth_url, data={
        "client_id": client_id
    })
    auth_url_data = {
        k: v[0] for k,v in parse_qs(auth_url_res.text).items()
    }

    debug("auth_url_data", auth_url_data)
    info(f"Please enter {auth_url_data['user_code']} at {auth_url_data['verification_uri']}. This code will expire in {(int(auth_url_data['expires_in']) + 1) / 60} mins")

    interval = int(auth_url_data["interval"])

    access_token_url = "https://github.com/login/oauth/access_token"
    access_token_payload = {
        "client_id": client_id,
        "device_code": auth_url_data.get("device_code", ""),
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
    }

    access_token_res = requests.post(url=access_token_url, data=access_token_payload)
    access_token_data = {
        k: v[0] for k,v in parse_qs(access_token_res.text).items()
    }
    debug("access_token_data", access_token_data)
    # doc: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app#about-user-access-tokens
    while "error" in access_token_data:
        sleep(interval)
        access_token_res = requests.post(url=access_token_url, data=access_token_payload)
        access_token_data = {
            k: v[0] for k,v in parse_qs(access_token_res.text).items()
        }
        debug("access_token_data", access_token_data)
    access_token = access_token_data["access_token"]
    return access_token
