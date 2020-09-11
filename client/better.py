import json
import platform

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from selenium.webdriver.support.wait import WebDriverWait

from client.worker import Worker


class Better(Worker):
    def __init__(self, task_queue):
        super().__init__(task_queue)
        self.skills = {"make_bet": self.make_bet,
                       "get_coefs": self.get_coefs}

    def login(self, name: str, password: str):
        driver = self.driver
        driver.get("https://1xstavka.ru/en/")
        driver.find_element_by_css_selector("[class='curloginDropTop base_auth_form']").click()
        driver.find_element_by_css_selector("[id='auth_id_email']").send_keys(name)
        driver.find_element_by_css_selector("[id='auth-form-password']").send_keys(password)
        driver.find_element_by_css_selector("button[class*='auth-button']").click()

        try:
            wait = WebDriverWait(driver, 10, poll_frequency=1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span[style*='border-bottom']")))
            text = driver.find_element_by_css_selector("span[style*='border-bottom']").text
            if text == "MY ACCOUNT":
                print("Logined succsessfull")
            else:
                print("Logined but something went wrong")
        except:
            print("Login failed")

    def get_coefs(self, game_link: str):
        driver = self.driver
        driver.get(game_link)

        commands_names = list(map(lambda x: x.text,
                                  driver.find_elements_by_css_selector("[class*='c-tablo__team']")))
        tablo_coefs = {commands_names[0]: dict(), commands_names[1]: dict()}

        tablo_rows = driver.find_elements_by_css_selector("[class='c-chart-stat c-tablo__chart']")

        for row in tablo_rows:
            name_coef = row.find_element_by_css_selector(
                "[class='c-chart-stat__title']").text
            left_coef = row.find_element_by_css_selector(
                "[class='c-chart-stat c-tablo__chart'] div:nth-child(2) div:nth-child(1)").text
            right_coef = row.find_element_by_css_selector(
                "[class='c-chart-stat c-tablo__chart'] div:nth-child(2) div:nth-child(3)").text
            tablo_coefs[commands_names[0]].update({name_coef: left_coef})
            tablo_coefs[commands_names[1]].update({name_coef: right_coef})

        total_cells = driver.find_elements_by_xpath("//*[normalize-space(text()) = 'Total']/../div[@class='bets "
                                                    "betCols2']/div")

        total_coefs = dict()
        for cell in total_cells:
            try:
                coef_name = cell.find_element_by_css_selector("[class = 'bet_type']").text
                coef_value = cell.find_element_by_css_selector("[class = 'koeff']").text
                total_coefs.update({coef_name: coef_value})
            except:
                pass

        result = {"Tablo": tablo_coefs, "Total": total_coefs}

        return result

    class MyListener(AbstractEventListener):
        def before_navigate_to(self, url, driver):
            print("Before navigate to %s" % url)

        def after_navigate_to(self, url, driver):
            print("After navigate to %s" % url)

    def check_changes(self, element: selenium.webdriver.remote.webelement.WebElement):
        driver = self.driver

        EventFiringWebDriver(driver_plain, MyListener())
        driver.after_change_value_of
        AbstractEventListener()

    def make_bet(self):
        return 0