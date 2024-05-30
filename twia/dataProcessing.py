# %%
import json
import pandas as pd
import numpy as np
import re
from datasets import load_dataset, ClassLabel, Sequence, Value, DatasetDict

# %%
def convertToConll(fileLoad, fileSave):
    """
    Takes data from doccano .jsonl and converts it to a conll format

    Inputs:
    - fileLoad: Location of .jsonl file
    - fileSave: Location of .csv in something approximating conll

    Outputs:
    - dfArtists: A .csv where:
        The first column is are sentences
        The second column is a list labeling each word 
    """
    with open(fileLoad, 'r') as json_file:
        json_list = list(json_file)

    for json_str in json_list:
        result = json.loads(json_str)
        # print(f"result: {result}")
        # print(isinstance(result, dict))
    text = result['text']
    labelIdx = result['label']

    # Get rid of all the text that isn't annotated yet
    lastLabel = labelIdx[-1][1]
    isLine = np.where(np.array(list(text)) == '\n')[0]
    isLine = isLine[isLine >= lastLabel]
    nextLine = isLine[0]
    text = text[0:nextLine]

    def findWhite(txt):
        txt = np.array(list(txt))
        isWhite = np.char.isspace(txt)
        isNotLine = txt != '\n'

        return isWhite & isNotLine 

    # First, label everything as O
    labelsChar = np.array(list('O'*len(text)))
    # Label spaces as spaces so we can split them later
    isWhite = findWhite(text)
    labelsChar[isWhite] = ' '
    labelsChar = ''.join(labelsChar)

    newText = text
    n = 0

    # Each sentence with a label is given a number
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
    newText = newText.split('\n')

    # We check each number portion to see if it's the beginning (B-band)
    # or the end/middle (I-band)
    encodings = []
    last = ''
    for sentence in newText:
        sentenceEncodings = []
        for word in sentence.split(' '):
            word = re.sub('[^A-Za-z0-9]+', '', word)
            if word.isnumeric():
                word = int(word[0])
                if word == last:
                    sentenceEncodings.append('I-band')
                else:
                    sentenceEncodings.append('B-band')
                last = word
            else:
                sentenceEncodings.append('O')
                last = -1
        encodings.append(sentenceEncodings)

    sentences = text.split('\n')

    # data cleaning in case there's a sentence of 0 length
    finalSentences, finalLabels = [], []
    for encoding, sentence in zip(encodings, sentences):
        if len(sentence) == 0:
            continue
        else:
            finalSentences.append(sentence)
            finalLabels.append(encoding)

    data = {'sentence': finalSentences, 'labels': finalLabels}
    dfArtists = pd.DataFrame(data)
    dfArtists.to_csv(fileSave, index = False, quoting = 1)
    
    return dfArtists

def makeDatasetDict(datasetLoc):
    """
    Loads a conll dataset and makes it a DatasetDict for huggingface
    Inputs:
    - datasetLoc: Location of csv from convertToConll
    Ouputs:
    - raw_datasets: A DatasetDict formatted dataset with training, testing, and validation slots
    """
    dataset = load_dataset('csv', data_files=datasetLoc)

    # Access the dataset
    ds = dataset['train']
    nerDict = {'O': 0, 'B-band': 1, 'I-band': 2}

    def process_labels(examples):
        # Convert the label strings to lists
        examples['labels'] = eval(examples['labels'])
        # Split sentences for tokenization
        examples['tokens'] = examples['sentence'].split()
        examples['ner_tags'] = [nerDict[val] for val in examples['labels']]
        return examples

    ds = ds.map(process_labels)

    new_features = ds.features.copy()
    ner_labels =['O', 'B-band', 'I-band']
    new_features['tokens'] = Sequence(feature=Value(dtype='string'), length=-1)
    new_features['labels'] = Sequence(feature=ClassLabel(names=ner_labels), length=-1)
    new_features['ner_tags'] = Sequence(feature=ClassLabel(names=ner_labels), length=-1)

    ds = ds.cast(new_features)
    trainTest = ds.train_test_split(test_size=0.2)
    testValid = trainTest['test'].train_test_split(test_size = 0.5)
    raw_datasets = DatasetDict({
        'train': trainTest['train'],
        'test' : testValid['test'],
        'validation': testValid['test']
    })

    return raw_datasets