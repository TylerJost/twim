# %%
import pandas as pd
from tqdm import tqdm
import random
import functools
import operator
import pickle
import matplotlib.pyplot as plt

from twia.getSpotify import levenshtein
from twia.getSpotify import scrapeAndClassifyArtists, levenshtein
from twia.getSpotify import authSpotify, authSpotifyClientCredentials

# %%
class artistInfo():
    """
    A class of information about an artist

    Attributes
    - artistName: The initial name of the artist
    - sp: Spotify authenticator
    - bestPredArtist: The closest artist that spotify can find
    - artistUri: Numerical code for the artist
    - topTracks: Information about the top 10 tracks for the artist
    """
    def __init__(self, artistName, sp):
        self.artistName = artistName
        self.sp = sp
        self.spotifyArtist, self.artistUri, self.artistInfo = self.searchSpotify()
        self.topTracks = self.getTopTracks()
    def searchSpotify(self):
        """
        Searches spotify using the artist name
        Accepts the artist if the levenshtein distance is less than 2
        """
        artistRes = self.sp.search(q=f'artist:{self.artistName}', type='artist')
        artistSearch = artistRes['artists']['items']
        spotifyArtist, artistUri = 'NaN', 'NaN'
        for potentialArtist in artistSearch:
            ld = levenshtein(self.artistName.lower(), potentialArtist['name'].lower())
            if ld <= 0:
                spotifyArtist = potentialArtist['name']
                artistUri = potentialArtist['uri']
                return spotifyArtist, artistUri, potentialArtist
        if len(artistSearch) > 0:
            artistInfo = artistSearch[0]
        else:
            artistInfo = 'NaN'
        return spotifyArtist, artistUri, artistInfo
    
    def getTopTracks(self):
        if self.artistUri != 'NaN':
            topTracks = self.sp.artist_top_tracks(self.artistUri)
            topTracks = topTracks['tracks']
        else:
            topTracks = 'NaN'                
        return topTracks
    
    def __repr__(self):
        return f'Artist: {self.artistName}\nSpotify Artist Name: {self.spotifyArtist}'
    def __str__(self):
        return f'Artist: {self.artistName}\nSpotify Artist Name: {self.spotifyArtist}'
# %%
showlistUrl = 'https://austin.showlists.net'
artistsPred = scrapeAndClassifyArtists(url = showlistUrl, maxDays = 7)
# %%
# Get artist information
# Here we use client credential authorizations for better rate limiting
# We also don't need to build the playlist yet
sp = authSpotifyClientCredentials()
# %%
allArtists = {}
i = 0
for artist in tqdm(artistsPred):
    predArtist = artistInfo(artist, sp)
    nTop = len(predArtist.topTracks)
    if predArtist.artistName != 'NaN' and nTop == 10:
        allArtists[artist] = predArtist
    # time.sleep(2)
    # if i > 5:
    #     break
    # i += 1
# %%
# A bit of analytics
popularityDf = {'name': [], 'popularity': []}

for artist in allArtists.values():
    popularityDf['name'].append(artist.artistName)
    popularityDf['popularity'].append(artist.artistInfo['popularity'])
popularityDf = pd.DataFrame(popularityDf).sort_values(by='popularity', ascending = False)
# %%
trackUris = {}
nTop = 15
topArtists = popularityDf['name'][0:nTop].to_list()
otherArtists = popularityDf['name'][nTop:].to_list()

random.shuffle(otherArtists)

c= 0
for artistName in topArtists:
    artist = allArtists[artistName]
    trackUris[artistName] = []
    for track in artist.topTracks[0:3]:
        trackUris[artistName].append(track['uri'])
        c += 1
for artistName in otherArtists[0:100-nTop*3]:
    artist = allArtists[artistName]
    trackUris[artistName] = [artist.topTracks[0]['uri']]
allUris = functools.reduce(operator.iconcat, trackUris.values(), [])
random.shuffle(allUris)
# %%
# sp = authSpotify()
# name = 'twia'
# description = "This week's music in Austin, TX"
# user_id = sp.me()['id']
# sp.user_playlist_create(user = user_id, 
#                         name=name,
#                         public = True,
#                         description=description)

# %%
playlistId = 'spotify:playlist:7oWlCMpyEMTjvu1GwIoDMN'
# %%
response = sp.playlist_items(playlistId,
                                offset=0,
                                fields='items.track.id,total',
                                additional_types=['track'])
# %%
sp.playlist_replace_items(playlistId, allUris)
# %%
# sp.playlist_add_items(playlist_id=playlistId, items=allUris)
# %%
spotifyArtists = [artist for artist in allArtists if artist.spotifyArtist != 'NaN']
# %%
import configparser
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials, CacheFileHandler

config = configparser.ConfigParser()

config.read('../../data/config.cfg')

CLIENT_ID = config['spotify']['client_id']
CLIENT_SECRET = config['spotify']['client_secret']
REDIRECT_URI = config['spotify']['redirect_uri']

username = 'tjost'
scope = 'playlist-modify-public'


CLIENT_ID = config['spotify']['client_id']
CLIENT_SECRET = config['spotify']['client_secret']
REDIRECT_URI = config['spotify']['redirect_uri']

cachePath = './.cache'
spOauth = SpotifyOAuth( 
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=scope,
            open_browser=False,
            cache_handler=CacheFileHandler(cachePath)
            )
token_info = spOauth.get_access_token()
sp = spotipy.Spotify(auth=token_info['access_token'])
# %%
cachePath = '.spotipyoauthcache'
sp_oauth  = SpotifyOAuth( 
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=scope,
            open_browser=False,
            cache_handler=CacheFileHandler(cachePath)
            )
token_info = sp_oauth.get_cached_token()

# %%
if not token_info:
    # If there is no cached token, prompt for authentication
    auth_url = sp_oauth.get_authorize_url()
    print(f'Please go to this URL to authorize: {auth_url}')
    response = input('Enter the URL you were redirected to: ')
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)
    if not token_info:
        raise Exception("Could not get token info")
    
# %%
if sp_oauth.is_token_expired(token_info):
    token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

# Save the token to the cache
sp_oauth.cache_handler.save_token_to_cache(token_info)

# Create a Spotipy client with the token
sp = spotipy.Spotify(auth=token_info['access_token'])

# Your Spotipy code here, for example:
results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(f'{idx + 1}. {track["name"]} by {track["artists"][0]["name"]}')