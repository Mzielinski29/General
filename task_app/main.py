import time
import argparse
import json
import sys
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
        print(f'{self.name} - created: {self.date}\n{self.status.value} - last modified: {time.ctime()}\n{self.content}')

    def edit_task_title(self, new_title):
        self.name = new_title
        self._update('title_change')
        save_task()

    def edit_task_content(self, new_content):
        msg = f'Are you sure you want to overwrite the content?\nWARNING! Current content will be lost [Yes/No/Cancel]: '
        user_action = ask_user(msg)

        while user_action != UserActions.CANCEL:
            if user_action == UserActions.YES:
                self.content = new_content
                self._update('content_change')
                save_task()
                return
            elif user_action == UserActions.NO:
                new_content = input('Enter the new content again: ')

            user_action = ask_user(msg)

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

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "tasks.json"
COMMANDS = ['add-task','show-task','show-all-tasks','edit-title','edit-content','change-status','task-history']


#--------------CONNECT JSON---------------

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

def show_all_tasks():

    if not TASKS:
        print("No tasks found.")
        return

    print("ID | Title | Status")
    print("-------------------")

    for task_id, task in TASKS.items():
        print(f'{task_id} | {task.name} | {task.status.value}')

def ask_user(msg):
    while True:
        answer = input(msg).strip().lower()

        try:
            return UserActions(answer)

        except ValueError:
            print('Invalid option.')

def require_args(command, *required):
    missing = []

    for arg in required:
        if getattr(args, arg) is None:
            missing.append(f'--{arg}')

    if missing:
        print(
            f'Command "{command}" requires: '
            + ", ".join(missing)
        )
        sys.exit()

def forbid_args(command, *forbidden):

    invalid = []

    for arg in forbidden:
        if getattr(args, arg) is not None:
            invalid.append(f'--{arg}')

    if invalid:
        print(
            f'Command "{command}" does not use: '
            + ", ".join(invalid)
        )
        sys.exit()


if __name__ == "__main__":

    load_tasks()

    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs='?')
    parser.add_argument("--id", type=int)
    parser.add_argument("--title")
    parser.add_argument("--content")
    parser.add_argument("--status")
    parser.add_argument("--commands",
                        help='show list of commands',
                        action='store_true')
    parser.add_argument("--usages",
                        help='examples of use',
                        action='store_true')

    args = parser.parse_args()

    if args.commands:
        print(f'list of commands:')
        for command in COMMANDS:
            print(f'\t{command}')
        sys.exit()
    elif args.usages:
        print(f'usage examples:\n\t[this_file] add-task --title "[title]" --content "[content]"\n\t[this_file] edit-title --title "[new_title]"')
        sys.exit()

    if args.command == 'add-task':
        require_args('add-task', 'title', 'content')
        forbid_args('id', 'status')
        task_id = create_task(args.title, args.content)
        print(f"Task created with ID {task_id}")
    elif args.command == 'show-task':
        require_args('show-task', 'id')
        task = get_task(args.id)
        if task:
            task.show_task()
    elif args.command == 'show-all-tasks':
        show_all_tasks()
    elif args.command == 'edit-title':
        require_args('edit-title', 'id', 'title')
        forbid_args('content', 'status')
        task = get_task(args.id)
        if task:
            task.edit_task_title(args.title)
    elif args.command == 'edit-content':
        require_args('edit-content', 'id', 'content')
        forbid_args('title', 'status')
        task = get_task(args.id)
        if task:
            task.edit_task_content()
    elif args.command == 'change-status':
        require_args('change-status', 'id', 'status')
        forbid_args('title', 'content')
        task = get_task(args.id)
        if task:
            task.change_task_status()
    elif args.command == 'task-history':
        require_args('task-history', 'id')
        forbid_args('title', 'content', 'status')
        task = get_task(args.id)
        if task:
            task.view_task_history()
    else:
        print(f'Invalid syntax\t try --help for usage or commands for list of commands')

