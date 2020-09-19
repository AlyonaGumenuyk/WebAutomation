import json
import time


class TaskManager:
    def __init__(self):
        self.tasks = dict()
        self.tasks_filepath = 'task_report/tasks.json'
        self.initialize_tasks_file()

    def initialize_tasks_file(self):
        with open(self.tasks_filepath, 'r+', encoding='utf8') as current_tasks:
            try:
                template = json.load(current_tasks)
            except:
                template = dict({'miner': [], 'better': []})
                json.dump(template, current_tasks, indent=4)

    def insert_tasks_file(self, task, worker_type):
        task = task.to_dict()
        with open(self.tasks_filepath, 'r', encoding='utf8') as tasks_file:
            data = json.load(tasks_file)
            new_data = data
            new_data[worker_type].append(task)
        with open(self.tasks_filepath, 'w', encoding='utf8') as tasks_file:
            tasks_file.write(json.dumps(new_data, indent=4))


