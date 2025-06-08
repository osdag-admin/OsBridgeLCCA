# Placeholder for input form UI
import json

def save_general_info(data, filename="src//osbridgelcca//desktop_app//assets//general_info.json"):
    """Save the general information dictionary to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)