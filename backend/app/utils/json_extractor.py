import json
import re

def extract_json(input: str):
    """
    Extract JSON from ```json``` code block in a file.
    """
    
    match = re.search(r"```json\n(.*?)\n```", input, re.DOTALL)
    if match:
        json_string = match.group(1)  # Extract JSON string
        data = json.loads(json_string)  # Parse JSON string
        return data, True
    else:
        return "", False