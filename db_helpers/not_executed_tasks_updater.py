import json
import time

from db_helpers.db_helper import DBHelper
from task_management.task import Task


class NotExecutedTasksUpdater(DBHelper):
    def __init__(self):
        super().__init__()
        self.delay = 60
        self.task_update()

    def task_update(self):
        while True:
            try:
                self.update_timeout()
                time.sleep(self.delay)
            except:
                time.sleep(self.conn_retry_delay)

