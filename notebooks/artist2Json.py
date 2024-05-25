# %%
import json
import pandas as pd
import numpy as np
# %%
from datasets import load_dataset
# raw_datasets = load_dataset("csv", data_files='../data/potterConll.csv')

raw_datasets = load_dataset("conll2003")
# %%
import json

with open('../data/artists.jsonl', 'r') as json_file:
    json_list = list(json_file)

for json_str in json_list:
    result = json.loads(json_str)
    # print(f"result: {result}")
    # print(isinstance(result, dict))
# %%

sentence_id, words, labels = [], [], []
text = result['text']
labelIdx = result['label']

bandNum = 1
for bandNum in range(0, 10):

    band = text[labelIdx[bandNum][0]: labelIdx[bandNum][1]]
    print(band)
bandParts = band.split()
# %%
def findWhite(txt):
    txt = np.array(list(txt))
    return np.char.isspace(txt)

# First, label everything as O
labelsChar = np.array(list('O'*len(text)))
# Label spaces as spaces
isWhite = findWhite(text)
labelsChar[isWhite] = ' '
labelsChar = ''.join(labelsChar)

newText = text
n = 0
for labelId in labelIdx:
    
    start = labelId[0]
    length = labelId[1] - labelId[0]
    newText = newText[:start] + str(n)*length + newText[start + length:]
    
    n += 1
    if n > 9:
        n = 0
newText = np.array(list(newText))
newText[isWhite] = ' '
newText = ''.join(newText)
newText = newText.split()
# %%
import re
encodings = []
last = ''
for word in newText:
    word = re.sub('[^A-Za-z0-9]+', '', word)
    if word.isnumeric():
        word = int(word[0])
        if word == last:
            encodings.append('I-band')
        else:
            encodings.append('B-band')
        last = word
    else:
        encodings.append('O')
        last = -1
    print(last)
# %%
stack = np.dstack([text.split(), encodings])
for val in stack[0][0:200]:
    print(val)