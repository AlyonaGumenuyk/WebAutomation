import datetime
import json
import time

import requests
from jsondiff import diff
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from client.diff_stat import DiffStat
from client.pages.match_page import MatchPage
from client.worker import Worker
from task_management.task import Task


class Better(Worker):
    def __init__(self):
        super().__init__()
        self.skills = {"make_bet": self.make_bet,
                       "watch": self.watch}
        self.worker_type = json.loads(json.dumps({'worker_type': 'better', 'tasks_number': 1}))

    def get_new_tasks(self):
        tasks = None
        while not tasks:
            tasks = requests.post(self.server_address + '/tasks', json=self.worker_type).json()
            if tasks:
                if self.driver:
                    self.reset_driver()
                for task in tasks:
                    print(task)
                    # task['params'] = json.loads(task['params'])
                    dt = datetime.datetime.strptime(task['params'][0], '%Y-%m-%d %H:%M:%S')
                    if datetime.datetime.now() - dt < datetime.timedelta(minutes=5):
                        self.task_queue.put(Task.to_task(task))
                    else:
                        task['params'] = []
                        self.task_queue.put(Task.to_task(task))
            else:
                print("sleeping for {} seconds while waiting for tasks".format(self.time_to_sleep))
                if self.driver:
                    self.driver.quit()
                time.sleep(self.time_to_sleep)

    def work(self):
        if self.task_queue.empty():
            self.get_new_tasks()
        task = self.task_queue.get()
        self.do_task(task)

    def do_task(self, task):
        if task.skill == 'watch':
            self.watch_match(task)

    def do_work(self):
        while True:
            try:
                self.work()
            except Exception as error:
                print(json.dumps("Sleeping for 10 sec, cause: " + str(error).strip().replace('\'', '\"')))
                time.sleep(10)
            finally:
                self.clean_logs()

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

    def watch_match(self, task: Task):
        match_page = MatchPage(driver=self.driver, better=self)
        server_adress = self.server_address + "/watch"
        differ = DiffStat()
        try:
            if not task.params:
                raise Exception('No sense to start watching match after 5 minutes')
            match_page.go_to_match(params=task.params)
            if match_page.match_is_finished():
                report = dict(
                    {"result": 'finished', "task_id": task.task_id, "skill": task.skill, "executed_state": 'success'})
                requests.post(self.server_address + "/watch", json=report)
            else:
                match_page.sort_table()
                prev_game_stat = dict()
                while not match_page.match_is_finished():
                    game_stat = self.watch(match_page)
                    if prev_game_stat:
                        changes = differ.diff(prev_stats=prev_game_stat, cur_stats=game_stat)
                        if changes:
                            report = dict({"result": changes, "task_id": task.task_id,
                                           "skill": task.skill, "executed_state": 'success'})
                            requests.post(self.server_address + "/watch", json=report)
                        prev_game_stat = game_stat
                    else:
                        report = dict({"result": game_stat, "task_id": task.task_id,
                                       "skill": task.skill, "executed_state": 'success'})
                        requests.post(self.server_address + "/watch", json=report)
                        prev_game_stat = game_stat
                    print("refreashing stats")
                    time.sleep(3)
                report = dict({"result": 'finished', "task_id": task.task_id,
                               "skill": task.skill, "executed_state": 'success'})
                requests.post(self.server_address + "/watch", json=report)

        except Exception as error:
            report = dict({"result": str(error).strip().replace('\'', '\"'), "task_id": task.task_id,
                           "skill": task.skill, "executed_state": 'error'})
            requests.post(server_adress, json=report)
            print(error)

    @staticmethod
    def watch(match_page: MatchPage):

        command_names = match_page.get_command_names()
        score = match_page.get_score()
        current_status = match_page.get_time()
        dashboard_coefs = match_page.get_dashboard_coefs()
        cards_and_penalties = match_page.get_cards_and_penalties()
        table_coefs = match_page.get_table_coefs()

        game_stat = dict()
        game_stat.update({"command_names": {"command_left": command_names[0], "command_right": command_names[1]}})
        game_stat.update({"score": {"command_left_score": score[0], "command_right_score": score[1]}})
        game_stat.update({"current_status": current_status})
        game_stat.update({"dashboard_coefs": dashboard_coefs})
        game_stat.update({'cards_and_penalties': cards_and_penalties})
        game_stat.update({"table_coefs": table_coefs})

        return game_stat

    @staticmethod
    def diff_stat(prev_stat: dict, cur_stat: dict):
        prev_stat_keys = prev_stat.keys()
        cur_stat_keys = cur_stat.keys()

        result = {'inserted coef groups': [], 'deleted coef groups': [],
                  'inserted coefs': [], 'deleted coefs': [], 'changed coefs': []}

        inserted_groups = cur_stat_keys - prev_stat_keys
        deleted_groups = prev_stat_keys - cur_stat_keys

    def make_bet(self):
        return 0
