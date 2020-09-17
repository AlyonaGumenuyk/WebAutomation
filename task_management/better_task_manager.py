import json
import threading
import time

from task_management.task_generator import TaskGenerator
from task_management.task_queue import TaskQueue
import os


class BetterTaskManeger:
    def __init__(self):
        self.task_queue = TaskQueue()

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def generate_watch_task(self):
        task = TaskGenerator.watch_gen(self.task_queue, 'https://1xstavka.ru/en/live/Football/118593-UEFA-Europa-League/256696089-Renova-Hajduk-Split/')

    def run(self):
        self.generate_watch_task()
