import json
import time

import requests
from jsondiff import diff
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from client.pages.match_page import MatchPage
from client.worker import Worker


class Better(Worker):
    def __init__(self, task_queue):
        super().__init__(task_queue)
        self.skills = {"make_bet": self.make_bet,
                       "get_coefs": self.get_coefs}

    @staticmethod
    def get_new_tasks():
        time_to_sleep = 10
        print("sleeping for {} seconds while waiting for tasks".format(time_to_sleep))
        time.sleep(time_to_sleep)

    def work(self):
        if self.task_queue.empty():
            self.get_new_tasks()
        task = self.task_queue.get()
        return self.do_task(task)

    def do_task(self, task):
        if task.method == 'watch':
            result = self.watch_match(task.params[0])
            return result

    def do_work(self):
        while True:
            result = self.work()
            if result == 'error':
                try:
                    report = json.loads(json.dumps({"Error": "Can not find the website"}))
                    requests.post('http://127.0.0.1:8081/get_coefs', json=report)
                except FileNotFoundError:
                    break

            elif result == 'finished':
                try:
                    report = json.loads(json.dumps({"Info": "Match is finished"}))
                    requests.post('http://127.0.0.1:8081/get_coefs', json=report)
                except FileNotFoundError:
                    break

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

    def watch_match(self, game_link: str):
        match_page = MatchPage(self.driver)

        try:
            match_page.go_to_site(game_link)
            if match_page.match_is_finished():
                return 'finished'
            match_page.sort_table()
        except:
            return 'error'

        prev_game_stat = dict()
        while not match_page.match_is_finished():
            game_stat = json.dumps(self.get_coefs(match_page))
            if game_stat == 'error':
                return game_stat
            try:
                if prev_game_stat:
                    changes = json.loads(diff(prev_game_stat, game_stat, load=True, dump=True))
                    print(changes)
                    status_changes = changes['current_status']
                    if len(changes) > 1 or list(status_changes.keys()) != ['time']:
                        print('sending')
                        requests.post('http://127.0.0.1:8081/get_coefs', json=changes)
                    prev_game_stat = game_stat
                else:
                    requests.post('http://127.0.0.1:8081/get_coefs', json=json.loads(game_stat))
                    prev_game_stat = game_stat
                print("refreashing stats")
                time.sleep(3)
            except FileNotFoundError:
                print("file not found")

        return 'finished'

    @staticmethod
    def get_coefs(match_page: MatchPage):

        command_names = match_page.get_command_names()
        score = match_page.get_score()
        current_status = match_page.get_time()
        dashboard_coefs = match_page.get_dashboard_coefs(command_names)
        table_coefs = match_page.get_table_coefs()

        game_stat = dict()
        game_stat.update({"command_names": {"command_left": command_names[0], "command_right": command_names[1]}})
        game_stat.update({"score": {"command_left_score": score[0], "command_right_score": score[1]}})
        game_stat.update({"current_status": current_status})
        game_stat.update({"dashboard_coefs": dashboard_coefs})
        game_stat.update({"table_coefs": table_coefs})

        return game_stat

    def make_bet(self):
        return 0
