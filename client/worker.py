import platform
import time

import requests
from selenium import webdriver
from task_management.task_queue import TaskQueue


class Worker:
    def __init__(self):
        self.task_queue = TaskQueue()
        if platform.system() == "Windows":
            print("Initializing Browser")
            self.driver = webdriver.Firefox(executable_path='../drivers/firefoxdriver/geckodriver.exe',
                                            log_path='../logs/geckodriver.log')
        else:
            self.driver = webdriver.Firefox(log_path='../logs/geckodriver.log')
        self.driver.set_window_size(1920, 1080)
        self.server_address = 'http://127.0.0.1:8081/'
        self.time_to_sleep = 10
