import json

# Open the input and output files
with open('test8.jsonl', 'r') as infile, open('output.jsonl', 'w') as outfile:
    # Read each line from the input file
    for line in infile:
        # Parse the JSON object
        data = json.loads(line)

        # Create a new JSON object in the desired format
        new_data = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a first aid certified bot. You are here to help with any first aid related questions."
                },
                {
                    "role": "user",
                    "content": data['prompt']
                },
                {
                    "role": "assistant",
                    "content": data['completion']
                }
            ]
        }

        # Write the new JSON object to the output file
        outfile.write(json.dumps(new_data) + '\n')