import json
import platform

import selenium
from flask import Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from selenium.webdriver.support.wait import WebDriverWait

from client.pages.base_page import BasePage
from client.pages.match_page import MatchPage
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
        match_page = MatchPage(self.driver)
        match_page.go_to_site(game_link)
        match_page.sort_table()
        command_names = match_page.get_command_names()
        score = match_page.get_score()
        dashboard_coefs = match_page.get_dashboard_coefs(command_names)
        table_coefs = match_page.get_table_coefs()

        game_stat = dict()
        game_stat.update({"command_names": {"command_left": command_names[0], "command_right": command_names[1]}})
        game_stat.update({"score": {"command_left_score": score[0], "command_right_score": score[1]}})
        game_stat.update({"dashboard_coefs": dashboard_coefs})
        game_stat.update({"table_coefs": table_coefs})

        return game_stat

    def make_bet(self):
        return 0
