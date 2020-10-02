import platform

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options

from task_management.task_queue import TaskQueue


class Worker:
    def __init__(self):
        self.task_queue = TaskQueue()
        if platform.system() == "Windows":
            options = Options()
            options.headless = True
            self.driver = webdriver.Firefox(executable_path='drivers/firefoxdriver/geckodriver.exe',
                                            log_path='logs/geckodriver.log')
            self.server_address = 'http://127.0.0.1:8000/'
        else:
            display = Display(visible=0, size=(1920, 1080))
            display.start()
            print('Initialized virtual display..')
            self.driver = webdriver.Firefox()
            self.server_address = 'http://0.0.0.0:8000/'
        self.window_length = 1920
        self.window_height = 1080
        self.driver.set_window_size(self.window_length, self.window_height)
        self.time_to_sleep = 10

    def scroll_to_element(self, element):
        if element.location['y'] > self.window_height:
            actions = ActionChains(self.driver)
            scroll_bar = self.driver.find_element_by_css_selector('[class="iScrollIndicator"]:nth-child(1)')
            scrolling_number = (1.1 * scroll_bar.size['height']) * (
                    element.location['y'] - scroll_bar.location['y']) / (
                                       1000 - scroll_bar.location['y']) - scroll_bar.size['height']
            actions.move_to_element(scroll_bar).click_and_hold() \
                .move_by_offset(0, scrolling_number).perform()

