from queue import Queue

from task_management.task import Task


class TaskQueue(Queue):
    def __init__(self, *args, **kwargs):
        super(TaskQueue, self).__init__(*args, **kwargs)

    def put(self, task_instance, **kwargs):
        if isinstance(task_instance, Task):
            super().put(task_instance)
        else:
            print('Not A Task')
