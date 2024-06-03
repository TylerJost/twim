# %%
from twia.getSpotify import authSpotify

sp = authSpotify()
# %%
results = sp.search(q='artist:' + 'Real Estate', type='artist')
# %%
uri = 'spotify:artist:41SQP16hv1TioVYqdckmxT'

topTracks = sp.artist_top_tracks(uri)
# %%
track = topTracks['tracks'][0]['uri']