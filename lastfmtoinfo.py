import requests
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
last_fm_key = os.getenv("LASTFM_KEY")
username = "humaneach"


def getTopTracks(page):
    r = requests.get(
        f"https://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user={username}&page={page}&limit=1000&api_key={last_fm_key}&format=json"
    )
    return r.json()


global names
global artists
global playcounts

names = []
artists = []
playcounts = []


def v(track):
    names.append(track["name"])
    artists.append(track["artist"]["name"])
    playcounts.append(track["playcount"])


def processPage(json_obj):
    arr = np.array(json_obj["toptracks"]["track"])
    vf = np.vectorize(v, otypes=[float])
    vf(arr)


page_1 = getTopTracks(1)
processPage(page_1)

max_pages = int(page_1["toptracks"]["@attr"]["totalPages"])


for i in range(2, max_pages + 1):
    page_i = getTopTracks(i)
    processPage(page_i)


df = pd.DataFrame({
    "names": names,
    "artists": artists,
    "playcounts": playcounts
})
df.to_csv(f"lastfminfo{username}.csv", index=False)
