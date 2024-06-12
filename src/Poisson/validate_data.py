import json

def validate_jsonl_in_chunks(file_path, chunk_size=1000):
    errors = []
    with open(file_path, 'r', encoding='utf-8') as file:
        chunk = []
        for line_number, line in enumerate(file, start=1):
            chunk.append(line)
            if line_number % chunk_size == 0:
                try:
                    # Attempt to load the chunk as a list of JSON objects
                    [json.loads(l) for l in chunk]
                except json.JSONDecodeError as e:
                    errors.append((line_number - chunk_size + 1, e))
                chunk = []
        # Check the last chunk
        if chunk:
            try:
                [json.loads(l) for l in chunk]
            except json.JSONDecodeError as e:
                errors.append((line_number - len(chunk) + 1, e))
    return errors

def load_jsonl_dataset(file_path):
    dataset = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            try:
                dataset.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error in line {line_number}: {e}")
                break
            except Exception as e:
                print(f"Unexpected error in line {line_number}: {e}")
                break
    return dataset

def in_colab(file_path):
    data=[]
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
        print(len(data))
        print(type(data[0]))


def get_max_lens(file_path):
    max_i = 0
    max_o = 0
    with open(file_path, 'r') as f: 
        for entry in f: 
            line = json.loads(entry)
            max_i = max(max_i, len(line['Input_Operators']))
            if len(line['Solution_Operators']) > max_o:
                max_o = len(line['Solution_Operators'])
    print(max_i, max_o)
# Attempt to load the entire dataset
# Display the number of successfully loaded lines

# Validate the JSONL file in chunks
# file_path = 'dataset.jsonl'
# errors = validate_jsonl_in_chunks(file_path)
# print(errors)
# dataset = load_jsonl_dataset(file_path)
# print(len(dataset))
# in_colab(file_path)
get_max_lens('dataset.jsonl')