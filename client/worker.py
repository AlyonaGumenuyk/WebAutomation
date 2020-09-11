import platform
from selenium import webdriver
from server.server import TaskQueue


class Worker:
    def __init__(self, task_queue: TaskQueue):
        self.task_queue = task_queue
        if platform.system() == "Windows":
            self.driver = webdriver.Chrome("../chromedriver/chromedriver.exe")
        else:
            # self.driver = webdriver.Chrome()
            self.driver = webdriver.Firefox()
        self.driver.set_window_size(1920, 1080)
