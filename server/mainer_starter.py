import threading

from client.miner import Mainer


class MainerStarter:
    def __init__(self, task_queue):
        self.task_queue = task_queue
        self.mainer = Mainer(task_queue)

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        self.mainer.do_work()
