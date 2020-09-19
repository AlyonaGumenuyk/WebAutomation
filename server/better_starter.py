import threading

from client.better import Better


class BetterStarter:
    def __init__(self):
        self.better = Better()

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        self.better.do_work()
