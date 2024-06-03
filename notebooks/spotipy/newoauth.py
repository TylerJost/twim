# %%
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from twia.getSpotify import authSpotify
# Ensure these values are correct
sp = authSpotify()
uri = 'spotify:artist:41SQP16hv1TioVYqdckmxT'

topTracks = sp.artist_top_tracks(uri)
