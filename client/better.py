import json
import time

import requests
from jsondiff import diff
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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
                for task in tasks:
                    print(task)
                    task['params'] = json.loads(task['params'])
                    self.task_queue.put(Task.to_task(task))
            else:
                print("sleeping for {} seconds while waiting for tasks".format(self.time_to_sleep))
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
                print("Sleeping")
                #print(error)
                time.sleep(10)

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
        try:
            match_page.go_to_match(params=task.params)
            if match_page.match_is_finished():
                report = json.loads(json.dumps(dict({"result": json.dumps('finished'), "task_id": task.task_id,
                                                     "skill": task.skill, "executed_state": 'success'})))
                requests.post(self.server_address + "/watch", json=report)
            else:
                match_page.sort_table()
                prev_game_stat = dict()
                while not match_page.match_is_finished():
                    game_stat = json.dumps(self.watch(match_page), ensure_ascii=False)
                    if prev_game_stat:
                        changes = json.loads(diff(prev_game_stat, game_stat, load=True, dump=True))
                        if changes and 'current_status' in changes.keys():
                            status_changes = changes['current_status']
                            print(list(changes.keys()))
                            if len(list(changes.keys())) > 1 or list(status_changes.keys()) != ['time']:
                                report = json.loads(json.dumps(dict({"result": changes, "task_id": task.task_id,
                                                                     "skill": task.skill, "executed_state": 'success'})))
                                requests.post(self.server_address + "/watch", json=report)
                            prev_game_stat = game_stat
                    else:
                        report = json.loads(json.dumps(dict({"result": game_stat, "task_id": task.task_id,
                                                             "skill": task.skill, "executed_state": 'success'})))
                        requests.post(self.server_address + "/watch", json=report)
                        prev_game_stat = game_stat
                    print("refreashing stats")
                    time.sleep(3)
                report = json.loads(json.dumps(dict({"result": json.dumps('finished'), "task_id": task.task_id,
                                                     "skill": task.skill, "executed_state": 'success'})))
                requests.post(self.server_address + "/watch", json=report)

        except Exception as error:
            report = json.loads(json.dumps(dict({"result": str(error).strip().replace('\'', '\"'),
                                                 "task_id": task.task_id, "skill": task.skill,
                                                 "executed_state": 'error'})))
            requests.post(server_adress, json=report)
            print(error)

    @staticmethod
    def watch(match_page: MatchPage):

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
