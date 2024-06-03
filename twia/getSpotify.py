import configparser
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os
import pathlib

def authSpotify():
    currentPath = pathlib.Path(__file__).resolve().parent
    config = configparser.ConfigParser()
    config.read(currentPath / '../data/config.cfg')

    CLIENT_ID = config['spotify']['client_id']
    CLIENT_SECRET = config['spotify']['client_secret']
    REDIRECT_URI = config['spotify']['redirect_uri']
    REDIRECT_URI = 'http://localhost:8000/callback'
    scope = "user-library-read"
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth( client_id=CLIENT_ID,
                                                    client_secret=CLIENT_SECRET,
                                                    redirect_uri=REDIRECT_URI,
                                                    scope=scope,
                                                    open_browser=False))
    return sp

def authSpotify2():
    currentPath = pathlib.Path(__file__).resolve().parent
    config = configparser.ConfigParser()
    config.read(currentPath / '../data/config.cfg')

    CLIENT_ID = config['spotify']['client_id']
    CLIENT_SECRET = config['spotify']['client_secret']
    REDIRECT_URI = config['spotify']['redirect_uri']

    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID,
                                            client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    return sp
