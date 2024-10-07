import json
import pandas as pd
import matplotlib.pyplot as plt

# File path
file_path = 'data/dataset.jsonl'

# Load the data and calculate entry lengths
entry_lengths = []

avg_solution = 0
lines = 0
with open(file_path, 'r') as file:
    for line in file:
        lines += 1
        entry = json.loads(line)
        entry_length = len(entry["Input_Operators"])
        avg_solution += len(set(entry['Solution_Operators']))
        entry_lengths.append(entry_length)

print('avg output len', avg_solution/lines)

# Plot the distribution of entry lengths
plt.figure(figsize=(10, 6))
plt.hist(entry_lengths, bins=50, color='blue', edgecolor='black')
plt.title('Distribution of Entry Lengths')
plt.xlabel('Number of Tokens')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
