# %%
import json
import pandas as pd
import numpy as np
import re
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
text = result['text']
labelIdx = result['label']
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
# %%
stack = np.dstack([text.split(), encodings])
for val in stack[0][0:200]:
    print(val)
# %%
sentenceNum = 0
lastNum = -1
isNewLine = np.array(list(text)) == '\n'
isWhiteOrLine = np.logical_or(isNewLine, isWhite)
sentenceNums = []
for val in text:

    if val == '\n':
        sentenceNums.append('\n')
        sentenceNum += 1
    elif val.isspace():
        sentenceNums.append(' ')

    else:
        if lastNum != sentenceNum:
            sentenceNums.append(str(sentenceNum))
            # print(sentenceNum)

        else:
            sentenceNums.append(':-1')
        lastNum = sentenceNum
sentenceNums = ''.join(sentenceNums).split()

sentenceNumsFinal = []
sentenceNum = 0
for sentence in sentenceNums:
    sentence = sentence.split(':')
    identifier = sentence[0]
    if identifier == '':
        sentenceNumsFinal.append(sentenceNum)
    elif int(identifier) == sentenceNum:
        sentenceNumsFinal.append(sentenceNum)
    else:
        sentenceNum += 1
        sentenceNumsFinal.append(sentenceNum)
print(sentenceNumsFinal)
# %%
print(len(sentenceNumsFinal))
print(len(encodings))
# %%
conllFormat = pd.DataFrame([sentenceNumsFinal, text.split(), encodings]).T
conllFormat.columns = ['sentence_id', 'words', 'labels']
conllFormat.to_csv('../data/conllArtists.csv', index = False)
# %%
from datasets import load_dataset
artistsDataset = load_dataset('csv', data_files='../data/conllArtists.csv')
artistsDataset
# %%
raw_datasets = load_dataset("conll2003")
raw_datasets["train"][0]
# %%
from datasets import load_dataset

# Load the dataset from the CSV file
dataset = load_dataset('csv', data_files='../data/conllArtists.csv')

# Function to group the words and labels by sentence_id
def group_by_sentence(examples):
    grouped_sentences = []
    grouped_labels = []
    current_sentence = []
    current_labels = []
    current_id = examples['sentence_id'][0]
    
    for i, sid in enumerate(examples['sentence_id']):
        if sid == current_id:
            current_sentence.append(examples['words'][i])
            current_labels.append(examples['labels'][i])
        else:
            grouped_sentences.append(current_sentence)
            grouped_labels.append(current_labels)
            current_sentence = [examples['words'][i]]
            current_labels = [examples['labels'][i]]
            current_id = sid
    
    grouped_sentences.append(current_sentence)
    grouped_labels.append(current_labels)
    
    return {'words': grouped_sentences, 'labels': grouped_labels}

# Apply the grouping function
dataset = dataset.map(group_by_sentence, batched=True, batch_size=len(dataset['train']), remove_columns=['sentence_id'])

# Now, you should have a dataset where each item is a sentence with corresponding words and labels
print(dataset)
