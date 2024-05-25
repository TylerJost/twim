# %%
from transformers import BertConfig, BertModel

# Building the config
config = BertConfig()

# Building the model from the config
model = BertModel(config)

print(config)

# Model is randomly intialized here
# %%
# this is pretrained
from transformers import BertModel

model = BertModel.from_pretrained("bert-base-cased")
# %%
model.save_pretrained(save_directory=".")

# %%
sequences = ["Hello!", "Cool.", "Nice!"]