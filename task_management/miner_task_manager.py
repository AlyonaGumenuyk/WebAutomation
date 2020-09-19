import json
import threading
import time

from task_management.task_generator import TaskGenerator
from task_management.task_manager import TaskManager


class MinerTaskManager(TaskManager):
    def __init__(self):
        super().__init__()
        self.worker_type = 'miner'
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def generate_tournaments_task(self):
        with open('task_report/tournaments.json', 'r+', encoding='utf8') as tournaments:
            tournaments.seek(0)
            tournaments.truncate()
        tournament_task = TaskGenerator.get_tournaments_gen('Chess')
        self.insert_tasks_file(tournament_task, self.worker_type)

    def generate_get_games_task(self):
        try:
            with open('task_report/tournaments.json', 'r+', encoding='utf8') as tournaments:
                current_tournaments = json.load(tournaments)
                for tournament_name, tournament_url in current_tournaments.items():
                    games_task = TaskGenerator.get_games_gen(tournament_url)
                    self.insert_tasks_file(games_task, self.worker_type)
            time.sleep(600)
        except json.decoder.JSONDecodeError:
            pass

    def run(self):
        while True:
            self.generate_tournaments_task()
            while True:
                self.generate_get_games_task()
            time.sleep(600)
