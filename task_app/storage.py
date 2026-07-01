import json
from pathlib import Path

def load_data(data_file):
    path = Path(data_file)

    if not path.exists():
        return {
            "next_id": 1,
            "tasks": []
        }

    with open(path, "r") as f:
        return json.load(f)
    
def save_data(data_file, data):
    with open(data_file, "w") as f:
        json.dump(data, f, indent=4)
