from pathlib import Path
from cli_handler import parse
import commands

#----------------MAIN BODY----------------

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "tasks.json"
COMMANDS = ['add-task','show-task','show-all-tasks','edit-title','edit-content','change-status','task-history']

if __name__ == "__main__":

    commands.load_tasks(DATA_FILE)

    args = parse()

    if args.commands:
        commands.commands_output(COMMANDS)
    elif args.usages:
        commands.usages_output()

    if args.command == 'add-task':
        commands.add_task(args)
    elif args.command == 'show-task':
        commands.show_task(args)
    elif args.command == 'show-all-tasks':
        commands.show_all_tasks()
    elif args.command == 'edit-title':
        commands.edit_title(args)
    elif args.command == 'edit-content':
        commands.edit_content(args)
    elif args.command == 'change-status':
        commands.change_status(args)
    elif args.command == 'task-history':
        commands.task_history(args)
    else:
        print(f'Invalid syntax\t try --help or --commands for list of commands / --usage for examples')

