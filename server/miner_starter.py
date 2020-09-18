import threading

from client.miner import Miner


class MinerStarter:
    def __init__(self, task_queue):
        self.task_queue = task_queue
        self.miner = Miner(task_queue)

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        self.miner.do_work()
