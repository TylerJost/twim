# %%
def nicePrint(dct):
    for item, amount in dct.items():  # dct.iteritems() in Python 2
        print(f"{item} ({amount})") 
# %%
# Here's how to train a sequence classifier on one batch with pytorch
import torch
from transformers import AdamW, AutoTokenizer, AutoModelForSequenceClassification

# Same as before
checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
sequences = [
    "I've been waiting for a HuggingFace course my whole life.",
    "This course is amazing!",
]
batch = tokenizer(sequences, padding=True, truncation=True, return_tensors="pt")

# This is new
batch["labels"] = torch.tensor([1, 1])

# AdamW is a modified Adam optimizer
optimizer = AdamW(model.parameters())
loss = model(**batch).loss
loss.backward()
optimizer.step()
# %%
# Access a dataset
from datasets import load_dataset

raw_datasets = load_dataset("glue", "mrpc")
raw_datasets
# %% Access each sentence
raw_train_dataset = raw_datasets["train"]

# %%
raw_train_dataset.features
# So label 0 corresponds to not_equivalent, 1 is equivalent
# %%
data = raw_train_dataset[15]

sen1 = data['sentence1']
sen2 = data['sentence2']
inputs = tokenizer(sen1, sen2)
nicePrint(inputs)
# %%
# We need to tokenize each dataset
from transformers import AutoTokenizer

checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
tokenized_sentences_1 = tokenizer(raw_datasets["train"]["sentence1"])
tokenized_sentences_2 = tokenizer(raw_datasets["train"]["sentence2"])

# We can also pass two setences
inputs = tokenizer('This is the first sentence.', "This is the second one.")
inputs

# Note there is now a token_type_ids part of inputs
# %%
tok = tokenizer.convert_ids_to_tokens(inputs["input_ids"])
tokenIds = inputs['token_type_ids']
import numpy as np
print(tok)
print(tokenIds)
# %%
# We can tokenize the whole dataset as well
tokenized_dataset = tokenizer(
    raw_datasets["train"]["sentence1"],
    raw_datasets["train"]["sentence2"],
    padding=True,
    truncation=True,
)
# This can take up a lot of RAM
# %%
