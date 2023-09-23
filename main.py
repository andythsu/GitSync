import requests
from urllib.parse import parse_qs

client_secret = "bbec7dfe54df734011ece4d35f0ff4c510afad4b"
client_id = "5fbc80938f0fa9cebefa"

def main():
    auth_url = "https://github.com/login/device/code"
    auth_url_res = requests.post(auth_url, data={
        "client_id": client_id
    })
    auth_url_res_data = {
        k: v[0] for k,v in parse_qs(auth_url_res.text).items()
    }
    print(auth_url_res_data)

if __name__ == "__main__":
    main()
