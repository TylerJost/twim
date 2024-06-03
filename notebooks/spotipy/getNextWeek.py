# %%
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import re
from tqdm import tqdm
from transformers import pipeline

# %% Define links and how to get data from them
def getShowlistArtists(url):
    'Gets artists from url and splits into list'
    res = requests.get(url)
    soup = BeautifulSoup(res.text)
    dateBands = soup.select('.show-link ,h5')
    dateBands = [line.text.replace('\n', '') for line in dateBands]
    dates = soup.select('h5')
    dates = [date.text.replace('\n', '') for date in dates]

    return dateBands, dates
def cleanDates(date):
    date = re.sub('\d+(st|nd|rd|th)', lambda m: m.group()[:-2].zfill(2), date)
    return datetime.strptime(date, '%A, %B %d %Y')
# %%
dateBands, dates = getShowlistArtists('https://austin.showlists.net')
# %%
output_dir = '../../models/bert-finetuned-ner'
# Replace this with your own checkpoint
model_checkpoint = output_dir
token_classifier = pipeline(
    "token-classification", model=model_checkpoint, aggregation_strategy="simple"
)
# %%
potentialArtists = token_classifier(dateBands[3])

# %%
allArtists = []
dt0 = cleanDates(dateBands[0])
for line in tqdm(dateBands):
    if line == 'List Filters':
        continue
    elif line in dates:
        dt = cleanDates(line)
        timeDiff = dt - dt0
        if timeDiff.days > 7:
            break
    else:
        potentialArtists = token_classifier(line)
        artists = []
        for artistPred in potentialArtists:
            if artistPred['score'] > 0.98:
                artists.append(artistPred['word'])
        allArtists += artists
# %%
artists = []
for artist in allArtists:
    if artist.endswith(','):
        artist = artist[0:-1]
    artist = artist.replace(' ’ ', "'")
    artists.append(artist)
# %%
from twia.getSpotify import authSpotify
artistRes = {}
sp = authSpotify()
# %%
i = 0
for artist in tqdm(artists):
    artistRes[artist] = sp.search(q=f'artist:{artist}', type='artist')
    i += 1
    if i > 50:
        break
# %%
results = sp.search(q='artist:' + 'Real Estate', type='artist')
