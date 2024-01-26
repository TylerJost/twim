# %%
from bs4 import BeautifulSoup
import requests
import pandas as pd
# %% Define links and how to get data from them
def getShowlistArtists(url):
    'Gets artists from url and splits into list'
    res = requests.get(url)
    soup = BeautifulSoup(res.text)
    artists = soup.select(".show-link")
    artists = [artist.text.replace('\n', '') for artist in artists]

    return artists, soup
urls = [
    'https://austin.showlists.net',
    'https://web.archive.org/web/20220520171603/https://austin.showlists.net/',
    'https://web.archive.org/web/20220819101041/https://austin.showlists.net/',
    'https://web.archive.org/web/20231011191423/https://austin.showlists.net/',
    'https://web.archive.org/web/20221126223609/https://austin.showlists.net/',
    'https://web.archive.org/web/20230204074147/https://austin.showlists.net/',
    'https://web.archive.org/web/20230614195140/https://austin.showlists.net/'
]
# %% Scrape artist data
bigSoup = []
allArtists = []

for url in urls:
    artists, soup = getShowlistArtists(url)
    allArtists += artists
    bigSoup.append(str(soup))
# %% Convert to writeable formats
bigSoup = [str(sp) for sp in bigSoup]
allSoup = '----------'.join(bigSoup)
allUniqueArtists = list(set(allArtists))
# %% Save data

# I save everything from the soup data so if I want to come back to it I can
with open('../data/trainingSoup.txt', 'w') as openFile:
    openFile.writelines(allSoup)

pd.DataFrame(allUniqueArtists).to_csv('../data/artistsTrain.csv')
