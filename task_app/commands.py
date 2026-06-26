from enums import UserActions
import sys
from storage import save_task, load_tasks
from task import Task

TASKS = {}
NEXT_ID = 1

def ask_user(msg):
    while True:
        answer = input(msg).strip().lower()

        try:
            return UserActions(answer)

        except ValueError:
            print('Invalid option.')

def create_task(name, content):
    global NEXT_ID

    task = Task(name, content)
    TASKS[NEXT_ID] = task

    task_id = NEXT_ID
    NEXT_ID += 1

    save_task()

    return task_id

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

def require_args(command, args, *required):
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

def forbid_args(command, args, *forbidden):

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

def commands_output(commands):
    print(f'list of commands:')
    for command in commands:
        print(f'\t{command}')
    sys.exit()

def usages_output():
    print(f'usage examples:\n\t[this_file] add-task --title "[title]" --content "[content]"\n\t[this_file] edit-title --title "[new_title]"')
    sys.exit()

def add_task(args):
    require_args('add-task', args, 'title', 'content')
    forbid_args('add-task', args, 'id', 'status')
    task_id = create_task(args.title, args.content)
    print(f"Task created with ID {task_id}")

def show_task(args):
    require_args('show-task', args, 'id')
    forbid_args('show-task', args, 'title', 'content', 'status')
    task = get_task(args.id)
    if task:
        task.show_task()

def edit_title(args):
    require_args('edit-title', args, 'id', 'title')
    forbid_args('edit-title', args, 'content', 'status')
    task = get_task(args.id)
    if task:
        task.edit_task_title(args.title)

def edit_content(args):
    require_args('edit-content', args, 'id', 'content')
    forbid_args('edit-content', args, 'title', 'status')
    task = get_task(args.id)
    if task:
        task.edit_task_content()

def change_status(args):
    require_args('change-status', args, 'id', 'status')
    forbid_args('change-status', args, 'title', 'content')
    task = get_task(args.id)
    if task:
        task.change_task_status()

def task_history(args):
    require_args('task-history', args, 'id')
    forbid_args('task-history', args, 'title', 'content', 'status')
    task = get_task(args.id)
    if task:
        task.view_task_history()