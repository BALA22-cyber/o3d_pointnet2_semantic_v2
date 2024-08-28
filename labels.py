import os
from collections import Counter

# Replace with the path to your folder containing the .labels files
input_folder_path = 'dataset/no_label_0.1'
output_folder_path = 'dataset/buildings_raw/corrected_labels'

# # List all .labels files in the directory
label_files = [f for f in os.listdir(input_folder_path) if f.endswith('.labels')]

# Function to count and print occurrences of labels in a file
def process_labels_file(file_path):
    with open(file_path, 'r') as file:
        labels = file.read().splitlines()
    labels = list(map(int, labels))
    label_counts = Counter(labels)
    return label_counts

# Process each .labels file
for label_file in label_files:
    file_path = os.path.join(input_folder_path, label_file)
    print(f"Processing file: {label_file}")
    label_counts = process_labels_file(file_path)
    for label, count in label_counts.items():
        print(f'Label {label}: {count} occurrences')
    print("\n" + "-"*40 + "\n")



"""######read and ignore the non- numeric lines and print the labels"""  
# label_files = [f for f in os.listdir(folder_path) if f.endswith('.labels')]

# # Function to count and print occurrences of labels in a file
# def process_labels_file(file_path):
#     with open(file_path, 'r') as file:
#         labels = file.read().splitlines()
#     # Convert labels to integers, ignoring non-numeric lines
#     labels = [int(label) for label in labels if label.isdigit()]
#     # Count the occurrences of each label
#     label_counts = Counter(labels)
#     return label_counts

# # Process each .labels file
# for label_file in label_files:
#     file_path = os.path.join(folder_path, label_file)
#     print(f"Processing file: {label_file}")
#     label_counts = process_labels_file(file_path)
#     for label, count in label_counts.items():
#         print(f'Label {label}: {count} occurrences')
#     print("\n" + "-"*40 + "\n")


""" read the non-numeric lines and write them in a new folder of the same format as semantic_3d labels"""

# # Create the output directory if it doesn't exist
# os.makedirs(output_folder_path, exist_ok=True)
# # List all .labels files in the directory
# label_files = [f for f in os.listdir(input_folder_path) if f.endswith('.labels')]
# # Function to clean and write labels to a new file
# def process_and_write_labels_file(input_file_path, output_file_path):
#     with open(input_file_path, 'r') as file:
#         labels = file.read().splitlines()
    
#     # Filter out non-numeric lines and convert labels to integers
#     cleaned_labels = [label for label in labels if label.isdigit()]
    
#     # Write the cleaned labels to a new file
#     with open(output_file_path, 'w') as file:
#         file.write("\n".join(cleaned_labels))

# # Process each .labels file
# for label_file in label_files:
#     input_file_path = os.path.join(input_folder_path, label_file)
#     output_file_path = os.path.join(output_folder_path, label_file)
#     print(f"Processing and writing file: {label_file}")
#     process_and_write_labels_file(input_file_path, output_file_path)

# print("Processing complete. Cleaned files saved to:", output_folder_path)
