import json

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_site(self, url):
        return self.driver.get(url)

    def close_page(self):
        self.driver.close()

    def freeze_page(self):
        self.driver.execute_script(
            "window.oldjQuery=window.jQuery;delete window.jQuery;delete "
            "window.$;window.oSend=XMLHttpRequest.prototype.send;XMLHttpRequest.prototype.send = function(){"
            "console.log('stopped ajax request', arguments)};")

    def unfreeze_page(self):
        self.driver.execute_script(
            "window.jQuery=window.oldjQuery;window.$=window.jQuery;XMLHttpRequest.prototype.send=window.oSend")

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                      message=json.dumps(
                                                          {"Error": f"Can't find element by locator {locator}"}))

    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                      message=json.dumps(
                                                          {"Error": f"Can't find elements by locator {locator}"}))
