import json
import threading
import time

from task_management.task_generator import TaskGenerator
from task_management.task_queue import TaskQueue
import os


class MinerTaskManeger:
    def __init__(self):
        self.tasks = dict()
        self.tasks_filepath = 'task_report/tasks.json'
        self.initialieze_tasks_file()

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def initialieze_tasks_file(self):
        with open(self.tasks_filepath, 'w') as current_tasks:
            template = dict({'miner': [], 'better': []})
            json.dump(template, current_tasks, indent=4)

    def generate_tournaments_task(self):
        with open('task_report/tournaments.json', 'r+') as tournaments:
            tournaments.seek(0)
            tournaments.truncate()
        tournament_task = TaskGenerator.get_tournaments_gen('Auto Race')
        self.insert_tasks_file(tournament_task, 'miner')

    def generate_get_games_task(self):
        try:
            with open('task_report/tournaments.json', 'r+') as tournaments:
                current_tournaments = json.load(tournaments)
                for tournament_name, tournament_url in current_tournaments.items():
                    games_task = TaskGenerator.get_games_gen(tournament_url)
                    self.insert_tasks_file(games_task, 'miner')
            time.sleep(600)
        except json.decoder.JSONDecodeError:
            pass

    def run(self):
        while True:
            self.generate_tournaments_task()
            while True:
                self.generate_get_games_task()
            time.sleep(600)

    def insert_tasks_file(self, task, worker_type):
        task = task.to_dict()
        with open(self.tasks_filepath, 'r') as tasks_file:
            data = json.load(tasks_file)
            new_data = data
            new_data[worker_type].append(task)
        with open(self.tasks_filepath, 'w') as tasks_file:
            tasks_file.write(json.dumps(new_data, indent=4))

    def update_tasks(self, worker_type):
        with open(self.tasks_filepath, 'r+') as current_tasks:
            try:
                data = json.load(current_tasks)
                data.update({worker_type: []})
                current_tasks.seek(0)
                current_tasks.truncate()
                json.dump(data, current_tasks, indent=4)
            except:
                time.sleep(1)
                data = json.load(current_tasks)
                data.update({worker_type: []})
                current_tasks.seek(0)
                current_tasks.truncate()
                json.dump(data, current_tasks, indent=4)
