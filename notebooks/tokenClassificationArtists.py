# %%
from datasets import load_dataset
# %%
raw_datasets = load_dataset('csv', data_files='../data/conllArtists.csv')


# %%
import pandas as pd
from datasets import load_dataset

# Create a DataFrame (for example purposes)
data = {
    "sentence": [
        "Hello John Doe",
        "How are you today ?"
    ],
    "labels": [
        '["B-PER", "I-PER", "I-PER"]',
        '["O", "O", "O", "O", "O"]'
    ]
}

df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv("token_classification_sentences.csv", index=False)

# Load the dataset
dataset = load_dataset('csv', data_files='token_classification_sentences.csv')

# Access the dataset
train_dataset = dataset['train']

# Convert the label strings to lists
def process_labels(examples):
    examples['labels'] = [eval(label) for label in examples['labels']]
    return examples

train_dataset = train_dataset.map(process_labels)

# Print some examples
for example in train_dataset[:2]:
    print(example)
