import json
import pandas as pd
import matplotlib.pyplot as plt

# File path
file_path = 'dataset.jsonl'

# Load the data and calculate entry lengths
entry_lengths = []

with open(file_path, 'r') as file:
    for line in file:
        entry = json.loads(line)
        entry_length = len(entry["Input_Operators"]) + len(entry["Solution_Operators"])
        entry_lengths.append(entry_length)

# Plot the distribution of entry lengths
plt.figure(figsize=(10, 6))
plt.hist(entry_lengths, bins=50, color='blue', edgecolor='black')
plt.title('Distribution of Entry Lengths')
plt.xlabel('Number of Tokens')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
