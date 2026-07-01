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
