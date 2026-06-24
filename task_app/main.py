import time
import argparse
import json
from pathlib import Path
import os
from enum import Enum

class TaskStatus(Enum):
    TODO = 'To Do'
    IN_PROGRESS = 'In Progress'
    FINISHED = 'Finished'
    ON_HOLD = 'On Hold'

class UserActions(Enum):
    YES = 'yes'
    NO = 'no'
    CANCEL = 'cancel'

class Task:
    def __init__(self, name, content):
        self.name = name
        self.date = time.ctime()
        self.status = TaskStatus.TODO
        self.content = content

        self.history = [{
            'action taken': 'create_task',
            'time': time.ctime(),
            'name': self.name,
            'status': self.status.value
        }]

    def __str__(self):
        return str(self.show_task())
    
    def _update(self, action):
        
        self.history.append({
            'action taken': action,
            'time': time.ctime(),
            'name': self.name,
            'status': self.status.value
        })

    def show_task(self):
        return f'{self.name} - created: {self.date}\n{self.status.value} - last modified: {time.ctime()}\n{self.content}'

    def edit_task_title(self, new_title):
        self.name = new_title
        self._update('title_change')
        save_task()

    def edit_task_content(self, new_content):
        user_action = ask_user()

        while user_action != UserActions.CANCEL:
            if user_action == UserActions.YES:
                self.content = new_content
                self._update('content_change')
                save_task()
                return
            elif user_action == UserActions.NO:
                new_content = input('Enter the new content again: ')

            user_action = ask_user()

    def change_task_status(self, new_status):
        self.status = new_status
        self._update('status_change')
        save_task()

    def view_task_history(self):
        print('-----------')
        for entry in self.history:
            for key, value in entry.items():
                print(f'{key}:\t{value}')
            print('-----------')

#----------------MAIN BODY----------------

TASKS = {}
NEXT_ID = 1
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "tasks.json"

def load_tasks():
    global TASKS, NEXT_ID

    if not os.path.exists(DATA_FILE):
        TASKS = {}
        NEXT_ID = 1
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    TASKS = {}
    for item in data["tasks"]:
        task = Task(item["name"], item["content"])
        task.date = item["date"]
        task.status = TaskStatus(item["status"])

        task.history = item["history"]
        TASKS[item["id"]] = task

    NEXT_ID = data["next_id"]

def create_task(name, content):
    global NEXT_ID

    task = Task(name, content)
    TASKS[NEXT_ID] = task

    task_id = NEXT_ID
    NEXT_ID += 1

    save_task()

    return task_id

def save_task():
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

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_task(task_id):
    return TASKS.get(task_id)

def ask_user():
    while True:
        #input for content change only, subject to change to var later
        answer = input(f'Are you sure you want to overwrite the content?\nWARNING! Current content will be lost [Yes/No/Cancel]: ').strip().lower()

        try:
            return UserActions(answer)

        except ValueError:
            print("Invalid option.")


if __name__ == "__main__":

    load_tasks()

    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("--id", type=int)
    parser.add_argument("--title")
    parser.add_argument("--content")

    args = parser.parse_args()

    if args.command == "add":
        task_id = create_task(args.title, args.content)
        print(f"Task created with ID {task_id}")
    elif args.command == "show":
        task = get_task(args.id)
        if task:
            task.show_task()
    elif args.command == "edit-title":
        task = get_task(args.id)
        if task:
            task.edit_task_title(args.title)
