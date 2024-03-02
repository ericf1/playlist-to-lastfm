import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
load_dotenv()

client_id = os.getenv("SPOTIFY_KEY")
client_secret = os.getenv("SPOTIFY_SECRET")

spotify = OAuth2Session(client_id, scope=[
    "playlist-read-private",
    "user-read-email",
    "playlist-read-collaborative"
], redirect_uri="http://localhost:3000/")

authorization_url, state = spotify.authorization_url(
    "https://accounts.spotify.com/authorize")
print('Please go here and authorize: ', authorization_url)
redirect_response = input('\n\nPaste the full redirect URL here: ')
# code = redirect_response.split("code=")[1].split("&")[0]
# r = requests.post(
#     "https://accounts.spotify.com/api/token",
#     data={
#         "code": code,
#         # redirect_uri: redirect_uri,
#         "grant_type": "authorization_code"
#     },
#     headers={
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Authorization': base64.urlsafe_b64encode((client_id + ': ' + client_secret).encode())
#     }
# )
# print(r.json())


auth = HTTPBasicAuth(client_id, client_secret)
token = spotify.fetch_token(
    "https://accounts.spotify.com/api/token",
    auth=auth,
    authorization_response=redirect_response)

print("\n" + token["access_token"])
