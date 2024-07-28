import json
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import defaultdict

# Load the JSON data from file
with open('output.json') as f:
    data = json.load(f)

# Initialize a dictionary to hold counts for each model
model_stats = defaultdict(lambda: {'TP': 0, 'FP': 0, 'TN': 0, 'FN': 0})

# Process each entry to populate model_stats
for entry in data:
    # Extract necessary fields
    try:
        message = entry.get('message', '{}')
        message_dict = ast.literal_eval(message)  # Convert string to dictionary
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing message field: {e}")
        continue

    model = message_dict.get('model', None)
    verified = message_dict.get('verified', None)
    test_image = message_dict.get('test_image', '')

    # Determine if test_image is criminal or innocent
    is_criminal = 'criminal' in test_image

    if verified:
        if is_criminal:
            model_stats[model]['FP'] += 1  # True Negative
        else:
            model_stats[model]['TP'] += 1  # False Negative
    else:
        if is_criminal:
            model_stats[model]['TN'] += 1  # False Positive
        else:
            model_stats[model]['FN'] += 1  # True Positive

# Function to plot and save diagonal confusion matrix
def plot_confusion_matrix_diagonal(stats, model_name):
    # Create confusion matrix DataFrame
    matrix = pd.DataFrame({
        'Predicted: Positive': [stats['TP'], stats['FP']],
        'Predicted: Negative': [stats['TN'], stats['FN']]
    }, index=['Actual: Positive', 'Actual: Negative'])
    
    # Plot confusion matrix with diagonal arrangement
    plt.figure(figsize=(6, 4))
    sns.heatmap(matrix, annot=True, fmt='d', cmap='Blues', cbar=False, square=True)
    plt.title(f'Confusion Matrix for Model: {model_name}')
    plt.savefig(f'confusion_matrix_{model_name}.png')
    plt.close()

# Plot and save confusion matrices for each model
for model, stats in model_stats.items():
    plot_confusion_matrix_diagonal(stats, model)

# Combine all matrices into a single confusion matrix
combined_stats = {'TP': 0, 'FP': 0, 'TN': 0, 'FN': 0}
for stats in model_stats.values():
    for key in combined_stats:
        combined_stats[key] += stats[key]

# Plot and save combined confusion matrix
plot_confusion_matrix_diagonal(combined_stats, 'Combined')
