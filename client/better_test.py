import datetime
import json
import time
from pprint import pprint

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

    def watch_match(self, task: Task):
        match_page = MatchPage(driver=self.driver, better=self)
        server_adress = self.server_address + "/watch"
        differ = DiffStat()
        try:
            if not task.params:
                raise Exception('No sense to start watching match after 5 minutes')
            match_page.go_to_match(params=task.params)
            if match_page.match_is_finished():
                print('match is finished')
            else:
                match_page.sort_table()
                prev_game_stat = dict()
                while not match_page.match_is_finished():
                    game_stat = self.watch(match_page)
                    if prev_game_stat:
                        changes = differ.diff(prev_stats=prev_game_stat, cur_stats=game_stat)
                        if changes:
                            print(changes)
                        prev_game_stat = game_stat
                    else:
                        prev_game_stat = game_stat
                        pprint(prev_game_stat)
                    print("refreashing stats")
                    time.sleep(3)

        except Exception as error:
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


if __name__ == '__main__':
    task_to_watch = {'task_id': 1234, 'skill': 'watch',
                     'params': ["2020-11-04 17:14:00", "Italy. Serie A", "Genoa", "Torino"],
                     'worker_type': 'better'}

    better_test = Better()
    better_test.watch_match(task=Task.to_task(task_to_watch))
