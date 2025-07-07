import os
import json
import csv

# Directory containing the JSON files
directory = "PATH_TO_LLM_OUTPUT"
output_file = "PATH_TO_extracted_data.csv"

# List to hold extracted data
data = []

# Iterate through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        filepath = os.path.join(directory, filename)
        print(f"Processing file: {filename}")
        with open(filepath, "r") as file:
            try:
                content = json.load(file)
                # Extract 'prompt' data
                url = None
                if "prompt" in content:
                    try:
                        prompt_data = json.loads(content["prompt"])  # Deserialize if it's a string
                        if isinstance(prompt_data, list) and len(prompt_data) > 0:
                            url = prompt_data[0].get("url")  # Extract URL
                    except (json.JSONDecodeError, TypeError):
                        print(f"Error parsing 'prompt' field in file: {filename}")
                
                # Extract 'response' data
                if "response" in content and isinstance(content["response"], dict):
                    try:
                        response_data = json.loads(content["response"]["response"])  # Deserialize JSON string
                        if isinstance(response_data, dict):
                            # Combine URL and response data into one row
                            row = {"url": url}
                            row.update(response_data)  # Add all keys from 'response'
                            data.append(row)
                    except (json.JSONDecodeError, TypeError):
                        print(f"Error parsing 'response' field in file: {filename}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")

# Write the extracted data to a CSV file
if data:
    # Dynamically determine all possible column names
    fieldnames = set()
    for row in data:
        fieldnames.update(row.keys())
    fieldnames = list(fieldnames)

    # Write data to CSV
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data successfully written to {output_file}")
else:
    print("No valid data found to write.")
