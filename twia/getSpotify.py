import configparser
import pathlib
from datetime import datetime
import re

import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

from transformers import pipeline

def authSpotify():
    currentPath = pathlib.Path(__file__).resolve().parent
    config = configparser.ConfigParser()
    config.read(currentPath / '../data/config.cfg')

    CLIENT_ID = config['spotify']['client_id']
    CLIENT_SECRET = config['spotify']['client_secret']
    REDIRECT_URI = config['spotify']['redirect_uri']
    scope = "user-library-read"
        
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth( client_id=CLIENT_ID,
                                                    client_secret=CLIENT_SECRET,
                                                    redirect_uri=REDIRECT_URI,
                                                    scope=scope,
                                                    open_browser=True))
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

def getShowlistArtists(url):
    "Gets artists and dates from url and splits into list"
    res = requests.get(url)
    soup = BeautifulSoup(res.text)
    dateBands = soup.select('.show-link ,h5')
    dateBands = [line.text.replace('\n', '') for line in dateBands]
    dates = soup.select('h5')
    dates = [date.text.replace('\n', '') for date in dates]

    return dateBands, dates

def cleanDates(date):
    "Converts dates from a general format, ie Monday, June 3rd 2024"
    date = re.sub('\d+(st|nd|rd|th)', lambda m: m.group()[:-2].zfill(2), date)
    return datetime.strptime(date, '%A, %B %d %Y')

def scrapeAndClassifyArtists(url = 'https://austin.showlists.net', maxDays = 7):
    """
    Scrape a given url and find artists within a given time period
    Inputs:
    - url: Url to scrape (only accepting austin.showlists.net right now)
    - maxDays: Max days in the future to search
    Outputs:
    - artists: Band names that are highly predicted to be actual bands
    """
    currentPath = pathlib.Path(__file__).resolve().parent

    dateBands, dates = getShowlistArtists(url)

    modelDir = currentPath / '../' / 'models/bert-finetuned-ner'

    token_classifier = pipeline(
        "token-classification", model=modelDir, aggregation_strategy="simple"
    )

    # Find artists in the appropriate range (maxDays)
    # Predict these with the BERT LLM
    allArtists = []
    dt0 = cleanDates(dateBands[0])
    for line in tqdm(dateBands):
        if line == 'List Filters':
            continue
        elif line in dates:
            dt = cleanDates(line)
            timeDiff = dt - dt0
            if timeDiff.days > maxDays:
                break
        else:
            potentialArtists = token_classifier(line)
            artists = []
            for artistPred in potentialArtists:
                if artistPred['score'] > 0.98:
                    artists.append(artistPred['word'])
            allArtists += artists

    artists = []
    for artist in allArtists:
        if artist.endswith(','):
            artist = artist[0:-1]
        artist = artist.replace(' ’ ', "'")
        artists.append(artist)

    return artists

def levenshtein(s1, s2):
    """
    Computes edit distance between s1 and s2 
    source:https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    """
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]