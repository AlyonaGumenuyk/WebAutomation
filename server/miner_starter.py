import threading

from client.miner import Miner


class MinerStarter:
    def __init__(self):
        self.miner = Miner()

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        self.miner.do_work()
