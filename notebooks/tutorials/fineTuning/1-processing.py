# %%
# This is one batch
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

# AdamW is an optimizer like Adam/SGD
optimizer = AdamW(model.parameters())
loss = model(**batch).loss
loss.backward()
optimizer.step()
# %%
from datasets import load_dataset

raw_datasets = load_dataset("glue", "mrpc")
raw_datasets

# %%
raw_train_dataset = raw_datasets["train"]
raw_train_dataset[0]
# %%
