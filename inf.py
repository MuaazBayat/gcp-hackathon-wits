import json
import ast
import matplotlib.pyplot as plt
from collections import defaultdict

def calculate_avg_inference_time_and_save_chart(file_path, output_image_path):
    # Load the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Dictionary to store total inference time and count for each model
    model_inference = defaultdict(lambda: {'total_time': 0.0, 'count': 0})
    
    # Process each entry in the JSON array
    for entry in data:
        # Parse the 'message' field to get a dictionary
        try:
            message_dict = ast.literal_eval(entry['message'])
        except (ValueError, SyntaxError):
            # Skip entries where message parsing fails
            continue
        
        # Extract the model name and inference time
        model = message_dict.get('model')
        inference_time = message_dict.get('inf_time')
        
        if model and inference_time is not None:
            # Update total time and count for the model
            model_inference[model]['total_time'] += inference_time
            model_inference[model]['count'] += 1
    
    # Calculate average inference times
    avg_inference_times = {}
    for model, stats in model_inference.items():
        avg_time = stats['total_time'] / stats['count'] if stats['count'] > 0 else 0
        avg_inference_times[model] = avg_time

    # Create a bar chart using matplotlib
    models = list(avg_inference_times.keys())
    avg_times = list(avg_inference_times.values())

    plt.figure(figsize=(10, 6))
    plt.bar(models, avg_times, color='skyblue')
    plt.xlabel('Model')
    plt.ylabel('Average Inference Time (seconds)')
    plt.title('Average Inference Time for Each Model')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the plot as an image file
    plt.savefig(output_image_path, format='png')

    # Optional: Show the plot (comment out if you only want to save the image)
    # plt.show()

# Replace 'your_file.json' with the path to your JSON file
# Replace 'output_chart.png' with the desired path for the output image file
calculate_avg_inference_time_and_save_chart('output.json', 'inference_chart.png')
