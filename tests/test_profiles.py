import requests


if __name__ == "__main__":

    url = "http://127.0.0.1:5000/players/profiles"

    args = {"profile": "Traditional Fullback"}

    request = requests.get(url=url, params=args)

    print(request.status_code)
    print(request.text)

