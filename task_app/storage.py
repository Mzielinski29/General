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

""" def load_tasks(data_file):

    if not os.path.exists(data_file):
        TASKS = {}
        NEXT_ID = 1
        return

    with open(data_file, "r") as f:
        data = json.load(f)

    TASKS = {}
    for item in data["tasks"]:
        task = Task(item["name"], item["content"])
        task.date = item["date"]
        task.status = TaskStatus(item["status"])

        task.history = item["history"]
        TASKS[item["id"]] = task

    NEXT_ID = data["next_id"]

def save_task(data_file):
    data = {
        "next_id": NEXT_ID,
        "tasks": []
    }

    for task_id, task in TASKS.items():
        data["tasks"].append({
            "id": task_id,
            "name": task.name,
            "date": task.date,
            "status": task.status.value,
            "content": task.content,
            "history": task.history
        })

    with open(data_file, "w") as f:
        json.dump(data, f, indent=4) """
