from dotenv import load_dotenv
import os
import requests
import json


load_dotenv()
token = os.getenv("TOKEN")
user_id = os.getenv("USER_ID")

r = requests.post(
    f"https://api.spotify.com/v1/users/{user_id}/playlists",
    headers={
        "Authorization": f"Bearer {token}"
    },
    data=json.dumps({
        "name": "Brandon's Anime Playlist Optimized",
        "description": "Created by Eric's Amazing Python Script",
        "public": True
    })
)

print(r.json()["id"])
