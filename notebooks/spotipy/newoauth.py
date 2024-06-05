# %%
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import configparser
from twia.getSpotify import authSpotify
# Ensure these values are correct
config = configparser.ConfigParser()
config.read('../../data/config.cfg')

CLIENT_ID = config['spotify']['client_id']
CLIENT_SECRET = config['spotify']['client_secret']
REDIRECT_URI = config['spotify']['redirect_uri']
REDIRECT_URI = 'https://www.example.org/callback'
scope = "user-library-read"

print(REDIRECT_URI)
auth_manager=SpotifyOAuth( client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                scope=scope,
                                                open_browser=True)
auth_url = auth_manager.get_authorize_url()
print("Authorize URL:", auth_url)
sp = spotipy.Spotify(auth_manager=auth_manager)
uri = 'spotify:artist:41SQP16hv1TioVYqdckmxT'

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(f"{idx+1}. {track['name']} by {track['artists'][0]['name']}")