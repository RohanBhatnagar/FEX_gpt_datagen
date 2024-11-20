def write_contents_to_new_file(source_file, destination_file):
    try:
        with open(source_file, 'r') as src:
            content = src.read()

        with open(destination_file, 'a') as dest:
            dest.write(content)

        print(f"Contents of {source_file} successfully written to {destination_file}")
    except FileNotFoundError:
        print(f"Error: {source_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


write_contents_to_new_file('data/Poisson_3dim_30000.jsonl', 'data/WaveHeatPoisson_data.jsonl')
