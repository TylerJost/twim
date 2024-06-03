# %%
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import re
from tqdm import tqdm
from transformers import pipeline
# %%
from twia.getSpotify import scrapeAndClassifyArtists, levenshtein
showlistUrl = 'https://austin.showlists.net'
artistsPred = scrapeAndClassifyArtists(url = showlistUrl, maxDays = 7)
# %%
from twia.getSpotify import authSpotify
artistRes = {}
sp = authSpotify()
# %%
i = 0
for artist in tqdm(artistsPred):
    artistRes[artist] = sp.search(q=f'artist:{artist}', type='artist')
    i += 1
    if i > 5:
        break
# %%
results = sp.search(q='artist:' + 'Real Estate', type='artist')
# %%
artists = artistRes.keys()
for artist in artists:
    artistSearch = artistRes[artist] 
# %%
spotifyArtists = artistSearch['artists']['items']
# %%
ld = 500
while ld > 2:
    break