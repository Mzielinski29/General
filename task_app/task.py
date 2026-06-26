import time
from enums import UserActions, TaskStatus
from storage import save_task
from cli_handler import ask_user

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