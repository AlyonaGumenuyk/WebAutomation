import json
import time

from db_helpers.db_helper import DBHelper
from task_management.task import Task


class TournamentsTaskGenerator(DBHelper):
    def __init__(self):
        super().__init__()
        self.delay = 60 * 60 * 24
        self.task_generation()

    def task_generation(self):
        while True:
            tournaments_task = self.get_tournaments_task('Football')
            self.insert_into_tasks(skill=tournaments_task.skill, arguments=json.dumps(tournaments_task.params),
                                   attempts=0, worker_type=tournaments_task.worker_type, state=self.task_init_state)
            time.sleep(self.delay)

    @classmethod
    def get_tournaments_task(cls, sport_name):
        return Task(skill='get_tournaments', params=[sport_name], worker_type='miner')
