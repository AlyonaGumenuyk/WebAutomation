import threading
import time

from task_management.task_generator import TaskGenerator
from task_management.task_manager import TaskManager


class BetterTaskManager(TaskManager):
    def __init__(self):
        super().__init__()
        self.worker_type = 'client'
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def generate_watch_task(self):
        watch_task = TaskGenerator.watch_gen(
            'https://1xstavka.ru/en/live/Football/225733-Russia-Premier-League/257066226-Ural-Zenit-Saint-Petersburg/')
        self.insert_tasks_file(watch_task, self.worker_type)

    def run(self):
        while True:
            self.generate_watch_task()
            time.sleep(3600)

