# %%
from datasets import load_dataset

raw_datasets = load_dataset("conll2003")
# %%
raw_datasets

# %%
raw_datasets["train"][0]["tokens"]
# %%
raw_datasets["train"][0]["ner_tags"]

# %%
ner_feature = raw_datasets["train"].features["ner_tags"]
ner_feature
# %%
label_names = ner_feature.feature.names
label_names
# %%
words = raw_datasets["train"][0]["tokens"]
labels = raw_datasets["train"][0]["ner_tags"]
line1 = ""
line2 = ""
for word, label in zip(words, labels):
    full_label = label_names[label]
    max_length = max(len(word), len(full_label))
    line1 += word + " " * (max_length - len(word) + 1)
    line2 += full_label + " " * (max_length - len(full_label) + 1)

print(line1)
print(line2)
# %%
from transformers import AutoTokenizer

model_checkpoint = "bert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
# %%
