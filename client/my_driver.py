import time
import pathlib

from selenium import webdriver

# Default for log_path variable. To be deleted when deprecations for arguments are removed.
DEFAULT_EXECUTABLE_PATH = "geckodriver"
DEFAULT_SERVICE_LOG_PATH = "geckodriver.log"
DEFAULT_LOG_PATH = "geckodriver.log"


class MyDriver(webdriver.Firefox):

    def __init__(self, executable_path=DEFAULT_EXECUTABLE_PATH,
                 service_log_path=DEFAULT_SERVICE_LOG_PATH,
                 log_path=DEFAULT_LOG_PATH,
                 options=None):
        super().__init__(executable_path=executable_path, service_log_path=service_log_path,
                         log_path=log_path, options=options)

    def get(self, url):
        super().get(url)
        super().execute_script("window.open('{}');".format(''))
        window_before = super().window_handles[0]
        window_after = super().window_handles[1]
        super().switch_to.window(window_before)
        super().execute_script('window.close()')
        super().switch_to.window(window_after)
        super().get(url)
