import json
import time

from db_helpers.db_helper import DBHelper
from db_helpers.task_manager import TaskManager
from task_management.task import Task


class WatchTaskGenerator(DBHelper):
    def __init__(self):
        super().__init__()
        self.delay = 10
        self.task_generation()

    def task_generation(self):
        while True:
            task_manager = TaskManager()
            games = task_manager.get_games_to_create_tasks()
            if games:
                for game in games:
                    watch_task = self.watch_task(str(game['datetime']), game['tournament'],
                                                 game['left_command'], game['right_command'])
                    existing_watch_tasks = json.loads(task_manager.get_tasks_for_execution(worker_type='better',
                                                                                           skill='watch'))
                    if existing_watch_tasks:
                        task_already_created = False
                        for existing_watch_task in existing_watch_tasks:
                            if watch_task.params == json.loads(existing_watch_task['params']):
                                task_already_created = True

                        if not task_already_created:
                            self.insert_into_tasks(skill=watch_task.skill, arguments=json.dumps(watch_task.params),
                                                   attempts=0, worker_type=watch_task.worker_type,
                                                   state=self.task_init_state)
                    else:
                        self.insert_into_tasks(skill=watch_task.skill, arguments=json.dumps(watch_task.params),
                                               attempts=0, worker_type=watch_task.worker_type,
                                               state=self.task_init_state)
                time.sleep(self.delay)
            else:
                time.sleep(self.delay)

    @classmethod
    def watch_task(cls, datetime, tournament, left_command, right_command):
        return Task(skill='watch', params=[datetime, tournament, left_command, right_command], worker_type='better')
