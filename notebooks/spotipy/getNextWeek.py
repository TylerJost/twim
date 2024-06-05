# %%
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import re
from tqdm import tqdm
from transformers import pipeline
import time
from twia.getSpotify import levenshtein
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
from twia.getSpotify import scrapeAndClassifyArtists, levenshtein
showlistUrl = 'https://austin.showlists.net'
# artistsPred = scrapeAndClassifyArtists(url = showlistUrl, maxDays = 7)
# %%
from twia.getSpotify import authSpotify
sp = authSpotify()
# %%
artists = []
i = 0
for artist in tqdm(artistsPred):
    artists.append(artistInfo(artist, sp))
    # time.sleep(2)
    if i > 5:
        break
    i += 1
# %%
artistName = 'HAAM'
spotifyArtistName = 'Haamin'
levenshtein(artistName.lower(), spotifyArtistName.lower())
# %%
artistFake = artistInfo('fakeasdf;lkjasdfh3lk', sp)
# %%
swift = sp.search(q=f'artist:King of Heck', type='artist')
swift = swift['artists']['items'][0]
# %%
pillar = sp.search(q=f'artist:Pillar', type='artist')
pillar = pillar['artists']['items'][0]

# %%
