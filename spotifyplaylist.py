import requests
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import jellyfish

load_dotenv()

token = os.getenv("TOKEN")
playlist_link = "https://open.spotify.com/playlist/2D2r0Wi6PxYvYHvCsQ96tt?si=5458d57f1c234572"

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
        names.append(item["track"]["name"])
        artists.append(item["track"]["artists"][0]["name"])
        ids.append(item["track"]["id"])

    length = len(playlist)
    i += 100

df = pd.DataFrame({
    "names": names,
    "artists": artists,
    "ids": ids,
})
df2 = pd.read_csv("lastfminfo.csv")


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

for i, r in df.iterrows():
    max_sim = -1
    final_names.append(r["names"])
    final_artists.append(r["artists"])
    final_ids.append(r["ids"])
    for i, r2 in df2.iterrows():
        sim = jellyfish.jaro_similarity(r["compare_str"], r2["compare_str"])
        if sim == 1:
            potential_final_playcount = r2["playcounts"]
            break
        if sim > max_sim:
            max_sim = sim
            potential_final_playcount = r2["playcounts"]
    final_playcounts.append(potential_final_playcount)

print(final_playcounts)

# final_df = pd.merge(df, df2, how="left", on="compare_str")
# final_df = final_df.sort_values(by=['playcounts'])
# final_df = final_df.drop("compare_str", axis=1)
# final_df.to_csv("toConvertToPlaylist.csv")
