# %%
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

print(SPOTIPY_CLIENT_ID)
print(SPOTIPY_CLIENT_SECRET)
print(SPOTIPY_REDIRECT_URI)




sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id    =SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri =SPOTIPY_REDIRECT_URI,
                                               scope        ="user-library-read"))