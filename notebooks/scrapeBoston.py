# %%
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import numpy as np

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
        if delta.days > 7:
            break
    else:
        if date in artistDates.keys():
            artistDates[date].append(entry)
        else:
            artistDates[date] = []

    
# %%
from twia.getSpotify import getShowlistArtists
url = 'https://austin.showlists.net'
dateBands, dates = getShowlistArtists(url)