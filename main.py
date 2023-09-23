from dataclasses import dataclass
from logging import debug
from time import sleep
from urllib.parse import parse_qs
from auth import get_access_token
import requests
import logger

logger.set_logging()

def main():
    access_token = get_access_token()
    return
    access_token = "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"
    url = "https://api.github.com/user"
    user_info = requests.get(url, headers={
        "Authorization": f"Bearer {access_token}"
    })
    user_info_json = user_info.json()
    owner = user_info_json["login"]
    debug(f"owner: {owner}")
    # get repo name
    repo_name = input("Enter the repo name you want to sync to: ")
    url = f"https://api.github.com/repos/{owner}/{repo_name}"
    repo_exists = requests.get(url, headers={
        "Authorization": f"Bearer {access_token}"
    })

    if repo_exists.status_code == 200:
        ...
    elif repo_exists.status_code == 404:
        ...

if __name__ == "__main__":
    main()
