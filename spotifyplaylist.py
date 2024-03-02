import requests
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import jellyfish

load_dotenv()

token = os.getenv("TOKEN")
playlist_link = "https://open.spotify.com/playlist/4zAtM3PGtgMbjAsUfqkwV4?si=992cd50f52744a7c"
lastfminfocsv = "lastfminfovortexual.csv"
# playlist_link = "https://open.spotify.com/playlist/06GSeylPe9AcW3691Nrz7i?si=c9ce8935b974419d"
playlist_id = playlist_link.split("/")[4].split("?")[0]

length = 100
i = 0
names = []
artists = []
ids = []
while length == 100:
    print(f"Getting 100 songs from the playlist...")
    r = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={i}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    s = r.json()
    playlist = s["items"]
    for item in playlist:
        try:
            names.append(item["track"]["name"])
            artists.append(item["track"]["artists"][0]["name"])
            ids.append(item["track"]["id"])
        except TypeError:
            print("This item has failed!")
            print(item)

    length = len(playlist)
    i += 100

df = pd.DataFrame({
    "names": names,
    "artists": artists,
    "ids": ids,
})
df2 = pd.read_csv(lastfminfocsv)


def v(nonalpha):
    string = [s for s in nonalpha if s.isalnum()]
    return "".join(string)


vf = np.vectorize(v)


df["compare_str"] = df["names"].str.lower() + df["artists"].str.lower()
df["compare_str"] = vf(df["compare_str"])

df2["compare_str"] = df2["names"].str.lower() + df2["artists"].str.lower()
df2["compare_str"] = vf(df2["compare_str"])
df2 = df2.drop("names", axis=1)
df2 = df2.drop("artists", axis=1)


# ok this is actually probably a useful implementation that I will use in the future
# Goal: join two columns by string similarity maximum similarity
final_names = []
final_artists = []
final_playcounts = []
final_ids = []


def vectorize_rows(compare_str, compare_strs, playcounts):
    sim = jellyfish.jaro_similarity(compare_str, compare_strs)
    return sim, playcounts


vfunc = np.vectorize(vectorize_rows)

print("Comparing all songs with each other and making the best match!")
for i, r in df.iterrows():
    final_names.append(r["names"])
    final_artists.append(r["artists"])
    final_ids.append(r["ids"])
    similarity, playcounts = vfunc(
        r["compare_str"], df2["compare_str"], df2["playcounts"])
    index = similarity.argmax(axis=0)
    final_playcounts.append(playcounts[index])

final_df = pd.DataFrame({
    "names": final_names,
    "artists": final_artists,
    "playcounts": final_playcounts,
    "ids": final_ids
})

final_df = final_df.sort_values(by=['playcounts'], ascending=False)
final_df.to_csv("toConvertToPlaylist.csv", index=False)
