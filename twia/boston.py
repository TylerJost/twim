# %%
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import numpy as np
from pathlib import Path
import pathlib
import re
import torch
from tqdm import tqdm
from transformers import pipeline
# %%
def bannedBostonVenue(venue):
    "Get rid of venues that aren't going to have artists/concerts"
    keywords = ['church', 'symphon', 'parish', 'berklee', 'conservatory', 'school of music']
    return any(word in venue.lower() for word in keywords)

def isVenue(entry):
    return entry.startswith('at') and entry.endswith(')')

def isEvent(entry):
    return not isVenue(entry)

def isDate(entry):
    days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    return entry.split(',')[0] in days

def getBostonSoup(url='https://bostonshows.org/'):
    res = requests.get(url)
    soup = BeautifulSoup(res.text)
    return soup

def removeBostonEvents(soup):
    eventsAndVenues = soup.select('.event-details div:nth-child(2) , #events div:nth-child(1)')

    allEvents, potentialBan = [], []
    for val in eventsAndVenues:
        val = val.text.replace('\n','')
        val = re.sub(r'\s+', ' ', val).strip()
        if isEvent(val):
            allEvents.append(val)
        elif isVenue(val):
            venue = val[3:].split(' (')[0]
            if bannedBostonVenue(venue):
                potentialBan.append(venue)
                if isEvent(lastVal):
                    potentialBan.append(lastVal)
        lastVal = val
    eventCt = pd.DataFrame(allEvents).value_counts()
    highEvent = eventCt[eventCt >2]
    highEvent = [event[0] for event in highEvent.index.to_list()]
    potentialBan += highEvent

    potentialBan = list(set(potentialBan))

    return potentialBan

def getClassifier():
    currentPath = pathlib.Path(__file__).resolve().parent
    modelDir = currentPath / '../' / 'models/bert-finetuned-ner'
    assert modelDir.exists(), f'{modelDir} not found'

    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    token_classifier = pipeline(
        "token-classification", 
        model=modelDir, 
        aggregation_strategy="simple",
        device = device
    )

    return token_classifier

def predArtists(soup, potentialBan, token_classifier, maxDays=7):
    webCommand = '.date-header , .event-details div:nth-child(2) , #events div:nth-child(1)'
    webFo = soup.select(webCommand)
    entries = [entry.text.replace('\n', '') for entry in webFo]
    firstDate = datetime.strptime(entries[0], "%A, %B %d")
    firstDate = firstDate.replace(day=datetime.now().day)

    predArtists = []
    isPast = 0
    for entry in tqdm(entries):
        # Check date
        if isDate(entry):
            date = datetime.strptime(entry, "%A, %B %d")
            delta = date - firstDate

            # If it's before the current date, continually skip
            if delta.days < 0:
                isPast = 1
            else:
                isPast = 0

            # Stop after a week
            if delta.days > maxDays:
                break
            continue

        # Don't do anything if the concert was in the past
        if isPast:
            continue

        if entry in potentialBan:
            continue
        

        if isEvent(entry):
            potentialArtists = token_classifier(entry)
            for potentialArtist in potentialArtists:
                if potentialArtist['score'] > 0.98:
                    predArtists.append(potentialArtist['word'])

    # Remove commas in artist at end of string
    artists = []
    for artist in predArtists:
        if artist.endswith(','):
            artist = artist[0:-1]
        artist = artist.replace(' ’ ', "'")
        artists.append(artist)

    return artists

def scrapeAndClassifyBoston(maxDays=7):
    print(f'\tScraping')
    soup = getBostonSoup()
    print(f'\tIdentifying removal events')
    potentialBan = removeBostonEvents(soup)
    token_classifier = getClassifier()
    print(f'\tPredicting artists for next {maxDays} days')
    artists = predArtists(soup, potentialBan, token_classifier, maxDays)

    return artists