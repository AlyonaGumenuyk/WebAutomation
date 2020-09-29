import json
import time

from db_helpers.db_helper import DBHelper
from db_helpers.task_manager import TaskManager
from task_management.task import Task


class GamesTaskGenerator(DBHelper):
    def __init__(self):
        super().__init__()
        self.delay = 60 * 60 * 12
        self.task_init_state = 'waiting for execution'
        self.task_generation()

    def task_generation(self):
        while True:
            try:
                self.get_tournaments_and_generate_tasks()
            except Exception as error:
                time.sleep(120)
                self.get_tournaments_and_generate_tasks()
            finally:
                time.sleep(self.delay)

    def get_tournaments_and_generate_tasks(self):
        task_manager = TaskManager()
        tournaments = json.loads(task_manager.get_tournaments())
        print(tournaments)
        if tournaments:
            for tournament_name, tournament_url in json.loads(tournaments['tournaments'])[0].items():
                print(tournament_name, tournament_url)
                games_task = self.get_games_task(tounament_url=tournament_url)
                self.insert_into_tasks(skill=games_task.skill, arguments=json.dumps(games_task.params),
                                       attempts=0, worker_type=games_task.worker_type, state=self.task_init_state)

    @classmethod
    def get_games_task(cls, tounament_url):
        return Task(skill='get_games', params=[tounament_url], worker_type='miner')
