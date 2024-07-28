import json
import ast
from collections import Counter

def count_models_from_json(file_path):
    # Load the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Initialize a counter for the models
    model_counter = Counter()
    
    # Iterate through each object in the JSON array
    for entry in data:
        # Parse the 'message' field to get a dictionary
        try:
            message_dict = ast.literal_eval(entry['message'])
        except (ValueError, SyntaxError):
            # Skip entries where message parsing fails
            continue
        
        # Extract the model name and increment the count
        model = message_dict.get('model')
        if model:
            model_counter[model] += 1
    
    # Print the results
    for model, count in model_counter.items():
        print(f"Model: {model}, Count: {count}")

# Replace 'your_file.json' with the path to your JSON file
count_models_from_json('output.json')
