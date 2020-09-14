import platform
from selenium import webdriver
from task_management.task_queue import TaskQueue


class Worker:
    def __init__(self, task_queue: TaskQueue):
        self.task_queue = task_queue
        if platform.system() == "Windows":
            print("Initializing Browser")
            self.driver = webdriver.Firefox(executable_path='../drivers/firefoxdriver/geckodriver.exe')
        else:
            self.driver = webdriver.Firefox()
        self.driver.set_window_size(1920, 1080)
