# %%
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import numpy as np
import re

from collections import defaultdict
# %%
url = 'https://bostonshows.org/'
res = requests.get(url)
soup = BeautifulSoup(res.text)
# %%
dateBands = soup.select('#events div:nth-child(1) , .sticky')
dateBands = [line.text.replace('\n', '') for line in dateBands]
# %%
days = ('Mon', 'Tue', 'Wed', 'Thu' 'Fri', 'Sat', 'Sun')
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
webBandLocs = soup.select('#events a , .event-details div:nth-child(2)')
c = 0
bandLocs = {}
for bandLoc in webBandLocs:
    bandLoc = bandLoc.text.replace('\n','')
    bandLoc = re.sub(r'\s+', ' ', bandLoc).strip()

    print(bandLoc)
    # if c == 0:
    #     bandLocs[bandLoc] = ''
    #     lastBand = bandLoc
    #     c = 1
    
    # if c == 1:
    #     if bandLoc.startswith('at') and bandLoc.endswith(')'):
    #         bandLoc = bandLoc[3:].split(' (')[0]
    #         bandLocs[lastBand] = bandLoc
    #     else:
    #         bandLocs[lastBand] = ''
    #     c = 0
