# playlist-to-lastfm

Convert a Spotify Playlist into its corresponding last.fm scribbles sorted.

Example env file:

```
LASTFM_KEY=
SPOTIFY_KEY=
SPOTIFY_SECRET=

TOKEN=
USER_ID=
NEW_PLAYLIST_ID=
```

## You are going to need your lastfm data (lastfmtoinfo.py)

1. Put in your desired username in the lastfmtoinfo.py script.
2. Run.

## You are going to need a Spotify OAuth 2.0 Token (spotify.py).

1. Run spotify.py and click on the link in the terminal.
2. Accept OAuth and then you will be redirected (it will say page not found but that doesn't matter)
3. Past that redirect link into the terminal prompt
4. It will give you the TOKEN and USER_ID
5. Input these into your .env

## You will now need to compare your Spotify Playlist and LastFM Data (spotifyplaylist.py).

1. Get the Spotify link that you desire to be searched and compared on and put it into spotify_link. There are examples in the file.
2. Input the correct csv file with the username into lastfminfocsv variable. It should be `f"lastfminfocsv{username}"`
3. Run.

## You are going to need a playlist ID to populate (createSpotifyPlaylist.py). If you do not have a playlist ID, create a playlist:

1. Populate the title and description
2. Run
3. Put the id that outputs in the terminal into your .env under NEW_PLAYLIST_ID

## You are going to populate the Spotify Playlist now (populatespotifyplaylist.py)

1. Ensure that you have the toConvertToPlaylist.csv file from spotifyplaylist.py and have inputed the NEW_PLAYLIST_ID env variable.
2. Run

## Now you should have that playlist populated organized from least scribbles to most scribbles

# Future

1. Think about better ways to compare strings/compress songs to get better results
2. Create a single main and a better flow
