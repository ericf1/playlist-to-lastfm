import requests
import os
from dotenv import load_dotenv
import pandas as pd
import json
import time

load_dotenv()
token = os.getenv("TOKEN")
user_id = os.getenv("USER_ID")
new_playlist_id = os.getenv("NEW_PLAYLIST_ID")
# converting the csv into a playlist in that order

df = pd.read_csv("toConvertToPlaylist.csv")

list_of_ids = df["ids"]
strings = []
for i in range(0, len(list_of_ids), 101):
    string = [f"spotify:track:{id}" for id in list(list_of_ids[i:i+100])]
    string = string[::-1]
    strings.append(string)


url = f"https://api.spotify.com/v1/playlists/{new_playlist_id}/tracks"
for s in strings:
    time.sleep(1)
    json_body = json.dumps({
        "uris": s,
        "position": 0
    })
    r = requests.post(
        url=url,
        data=json_body,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    print(r.json())
