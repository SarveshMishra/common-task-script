import json
import requests
import base64

# Define the Consul API URL
consul_url = "http://consul_url:8500/v1/kv/"

# Define the path to your JSON file
json_file_path = './response.json'

# Read and process data from the JSON file line by line
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Iterate through the JSON objects
for item in data:
    key = item.get("Key")
    base64_value = item.get("Value")

    # Ensure key and base64_value are not empty
    if key is not None and base64_value is not None:
        try:
            # Decode the base64 string to bytes and then convert to a string
            decoded_value = base64.b64decode(base64_value).decode('utf-8')

            # Send a PUT request to Consul to create/update the key-value pair
            response = requests.put(consul_url + key, data=decoded_value)

            # Check if the request was successful
            if response.status_code == 200:
                print(f"Key-value pair '{key}' added/updated successfully in Consul.")
            else:
                print(f"Failed to add/update key-value pair '{key}' in Consul. Status code: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"Error decoding base64 value for key '{key}': {str(e)}")
    else:
        print("Skipping object with missing 'key' or 'value'.")
