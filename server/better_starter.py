import threading

from client.better import Better


class BetterStarter:
    def __init__(self, task_queue):
        self.task_queue = task_queue
        self.better = Better(task_queue)

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        self.better.do_work()
