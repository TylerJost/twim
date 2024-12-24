# %%
import requests
import pickle
# %%
url = 'https://bostonshows.org/'
res = {}
res['boston'] = requests.get('https://bostonshows.org/')
res['austin'] = requests.get('https://austin.showlists.net/')
# with open('res.pkl', 'wb') as f:
#     pickle.dump(res, f)
# %%
with open('res.pkl', 'rb') as f:
    res = pickle.load(f)
# %%
from bs4 import BeautifulSoup
soup = BeautifulSoup(res['boston'].text)