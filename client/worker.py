import platform

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from task_management.task_queue import TaskQueue
from pyvirtualdisplay import Display


class Worker:
    def __init__(self):
        self.task_queue = TaskQueue()
        if platform.system() == "Windows":
            options = Options()
            options.headless = True
            self.driver = webdriver.Firefox(executable_path='drivers/firefoxdriver/geckodriver.exe',
                                            log_path='logs/geckodriver.log', options=options)
            self.server_address = 'http://127.0.0.1:8000/'
        else:
            display = Display(visible=0, size=(1920, 1080))
            display.start()
            print('Initialized virtual display..')
            self.driver = webdriver.Firefox()
            self.server_address = 'http://0.0.0.0:8080/'
        self.driver.set_window_size(1920, 1080)
        self.time_to_sleep = 10
