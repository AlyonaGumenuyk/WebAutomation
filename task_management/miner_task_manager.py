import json
import threading
import time

from task_management.task_generator import TaskGenerator
from task_management.task_queue import TaskQueue
import os


class MinerTaskManeger:
    def __init__(self):
        self.task_queue = TaskQueue()

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def generate_tournaments_task(self):
        task = TaskGenerator.get_tournaments_gen(self.task_queue)

    def generate_get_games_task(self):
        try:
            with open('task_report/tournaments.json', 'r') as tournaments:
                current_tournaments = json.load(tournaments)
                for tournament_name, tournament_url in current_tournaments.items():
                    TaskGenerator.get_games_gen(self.task_queue, tournament_url)
            with open('task_report/tournaments.json', 'w') as tournaments:
                tournaments.seek(0)
                tournaments.truncate()
            time.sleep(600)
        except json.decoder.JSONDecodeError:
            pass

    def run(self):
        while True:
            self.generate_tournaments_task()
            while True:
                self.generate_get_games_task()
            time.sleep(600)
