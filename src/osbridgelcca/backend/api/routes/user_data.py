import json
from pathlib import Path

# Placeholder for user data
def save_user_input(data):
    output_path = Path(__file__).parent / "user_input.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
