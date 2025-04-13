# %%
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import numpy as np
import re
# %%
url = 'https://bostonshows.org/'
res = requests.get(url)
soup = BeautifulSoup(res.text)
# %%
dateBands = soup.select('#events div:nth-child(1) , .sticky')
dateBands = [line.text.replace('\n', '') for line in dateBands]
# %%
days = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
artistDates = {}

firstDate = datetime.strptime(dateBands[0], "%a, %B %d")

for entry in dateBands:
    # Check date
    entryDay = entry.split(',')[0]
    if entryDay in days:
        date = datetime.strptime(entry, "%a, %B %d")
        delta = np.abs(date - firstDate)
        # if delta.days > 7:
        #     break
    else:
        if date in artistDates.keys():
            artistDates[date].append(entry)
        else:
            artistDates[date] = []
# %%
# Find recurring events
allEvents = []
for date, artist in artistDates.items():
    allEvents+= artist
uniqueEvents, cts = np.unique(allEvents, return_counts=True)
recurEvents = []
eventDict = {}
for event, ct in zip(uniqueEvents, cts):
    event = str(event)
    if ct >= 4:
        recurEvents.append(str(event))
        eventDict[event] = ct
# %%
import torch
modelDir = '../models/bert-finetuned-ner'
from transformers import pipeline

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
token_classifier = pipeline(
    "token-classification", 
    model=modelDir, 
    aggregation_strategy="simple",
    device = device
)
# %%
from tqdm import tqdm

c = 0
predArtists = {}
for event in tqdm(allEvents):
    if event in recurEvents:
        continue
    potentialArtists = token_classifier(event)
    for potentialArtist in potentialArtists:
        if potentialArtist['score'] > 0.98:
            predArtists[event] = potentialArtist['word']
    c += 1
    if c > 100:
        break

for artist, pred in predArtists.items():
    print(f'{artist}\n\t{pred}\n')
# %%
from pprint import pprint
# webBandLocs = soup.select('#events a , .event-details div:nth-child(2)')
webBandLocs = soup.select('.event-details div:nth-child(2) , #events div:nth-child(1)')
wasBand = 0
bandLocs = {}
lastEntry = ''
def isLocation(entry):
    return entry.startswith('at') and entry.endswith(')')
def isBand(entry):
    return not isLocation(entry)

for bandLoc in webBandLocs:
    bandLoc = bandLoc.text.replace('\n','')
    bandLoc = re.sub(r'\s+', ' ', bandLoc).strip()

    # If it's a band, store with empty string
    if isBand(bandLoc):
        bandLocs[bandLoc] = ''
    # If it's a location and the last one was a band
    if isLocation(bandLoc) and isBand(lastEntry):
        bandLocs[lastEntry] = bandLoc[3:].split(' (')[0]


    lastEntry = bandLoc
# %%
# Make e
allVenues = list(bandLocs.values())
potentialBan = []

def bannedVenue(venue):
    return any(word in venue.lower() for word in ['church', 'symphon', 'parish', 'berklee', 'conservatory', 'school of music'])
for venue in allVenues:
    if bannedVenue(venue):
        potentialBan.append(venue)

potentialBan = list(set(potentialBan))

venueCt = pd.DataFrame(allVenues).value_counts()

bands = []
for bandLoc in webBandLocs:
    bandLoc = bandLoc.text.replace('\n','')
    bandLoc = re.sub(r'\s+', ' ', bandLoc).strip()
    if isBand(bandLoc):
        bands.append(bandLoc)

        if 'symphon' in bandLoc.lower():
            potentialBan.append(bandLoc)
eventCt = pd.DataFrame(bands).value_counts()
highEvent = eventCt[eventCt >2]
highEvent = [event[0] for event in highEvent.index.to_list()]
potentialBan += highEvent
# %%
# Try to get the dates in there too
webCommand = '.date-header , .event-details div:nth-child(2) , #events div:nth-child(1)'
webFo = soup.select(webCommand)
entries = [entry.text.replace('\n', '') for entry in webFo]
firstDate = datetime.strptime(entries[0], "%a, %B %d")
firstDate = firstDate.replace(day=datetime.now().day)

def isLocation(entry):
    return entry.startswith('at') and entry.endswith(')')
def isBand(entry):
    return not isLocation(entry)
def isDate(entry):
    days = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    return entry.split(',')[0] in days
predArtists = []
isPast = 0
for entry in tqdm(entries):
    # Check date
    if isDate(entry):
        date = datetime.strptime(entry, "%a, %B %d")
        delta = date - firstDate

        # If it's before the current date, continually skip
        if delta.days < 0:
            isPast = 1
        else:
            isPast = 0

        # Stop after a week
        if delta.days > 7:
            break
        continue

    # Don't do anything if the concert was in the past
    if isPast:
        continue

    if entry in potentialBan:
        continue
    

    if isBand(entry):
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