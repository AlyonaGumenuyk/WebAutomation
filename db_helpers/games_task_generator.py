import json
import time

from db_helpers.db_helper import DBHelper
from task_management.task import Task


class GamesTaskGenerator(DBHelper):
    def __init__(self):
        super().__init__()
        self.delay = 60 * 60 * 12
        self.task_init_state = 'waiting for execution'
        self.task_generation()

    def insert_into_tasks(self, skill, arguments, attempts, worker_type, state):
        self.connect(self.stavka_db)
        if self.conn:
            try:
                task = f"""
                INSERT INTO tasks (skill, arguments, attempts, worker_type, state) 
                VALUES ('{skill}', '{arguments}', {attempts}, '{worker_type}', '{state}')
                """
                self.cur.execute(task)
                self.conn.commit()
                print('Task has been inserted')
            except Exception as error:
                print("Failed to insert record into tasks table", error)
            finally:
                self.close_connection()

    def task_generation(self):
        while True:
            tournaments_task = self.get_tournaments_task('Football')
            self.insert_into_tasks(skill=tournaments_task.skill, arguments=json.dumps(tournaments_task.params),
                                   attempts=0, worker_type=tournaments_task.worker_type, state=self.task_init_state)
            time.sleep(self.delay)

    @classmethod
    def get_tournaments_task(cls, sport_name):
        return Task('get_tournaments', [sport_name], 'miner')
