# %%
tokenized_text = "Jim Henson was a puppeteer".split()
print(tokenized_text) 
# Could also split on punctuation, etc
# %%
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
# %%
tokenizer("Using a Transformer network is simple")
# tokenizer.save_pretrained("directory_on_my_computer")
# %% Encoding
# Encoding is tokenization, then conversion to input ids

# Tokenization
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

sequence = "Using a jost Transformer network is simple"
tokens = tokenizer.tokenize(sequence)

print(tokens)

# Convert to ids
ids = tokenizer.convert_tokens_to_ids(tokens)

print(ids)

decoded_string = tokenizer.decode(ids)
print(decoded_string)