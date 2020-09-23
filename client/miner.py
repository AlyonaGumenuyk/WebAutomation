import json
import time
import requests

from datetime import datetime
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from client.worker import Worker
from task_management.task import Task


class Miner(Worker):
    def __init__(self):
        super().__init__()
        self.skills = {"get_tournaments": self.get_tournaments,
                       "get_games": self.get_games}
        self.worker_type = json.loads(json.dumps({'worker_type': 'miner'}))

    def get_new_tasks(self):
        tasks = None
        while not tasks:
            tasks = requests.post(self.server_address + '/tasks', json=self.worker_type).json()
            if tasks:
                for task in tasks:
                    print(task)
                    self.task_queue.put(Task.to_task(task))
            else:
                print("sleeping for {} seconds while waiting for tasks".format(self.time_to_sleep))
                time.sleep(self.time_to_sleep)

    def work(self):
        if self.task_queue.empty():
            self.get_new_tasks()
        task = self.task_queue.get()
        return self.do_task(task)

    def do_task(self, task):
        if task.method == 'get_tournaments':
            try:
                report = self.get_tournaments(task.params[0])
                result = dict(
                    {"server_adress": self.server_address + "/tournaments", "report": report})
            except Exception as er:
                result = dict(
                    {"server_adress": self.server_address + "/report", "report": "error",
                     "error_description": str(er).strip(),
                     "time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S:%f"), "task": task.method})
        elif task.method == 'get_games':
            try:
                report = self.get_games(task.params[0])
                result = dict({"server_adress": self.server_address + "/games", "report": report})
            except Exception as er:
                result = dict(
                    {"server_adress": self.server_address + "/report", "report": "error",
                     "error_description": str(er).strip(),
                     "time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S:%f"), "task": task.method})
        else:
            result = dict({"server_adress": self.server_address + "/report", "report": "unknown task name",
                           "task": task.method, "time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S:%f")})
        return result

    def do_work(self):
        while True:
            try:
                result = self.work()
                if result["report"] == 'error':
                    try:
                        report = json.loads(json.dumps({"Error in " + result["task"]: result["error_description"],
                                                        "Time": result["time"]}))
                        requests.post(result["server_adress"], json=report)
                    except Exception as er:
                        print(er, "in 'error' handling")
                elif result["report"] == 'unknown task name':
                    try:
                        report = json.loads(json.dumps({"Error": "Unknown task name",
                                                        "Time": result["time"]}))
                        requests.post(result["server_adress"], json=report)
                    except Exception as er:
                        print(er, "in 'unknown task name' handling")
                else:
                    try:
                        report = json.loads(json.dumps(result["report"]))
                        requests.post(result["server_adress"], json=report)
                    except Exception as er:
                        print(er, "in normal work")
            except:
                print("Sleeping")
                time.sleep(10)

    def get_tournaments(self, sport_name: str):
        result = dict()

        driver = self.driver
        driver.get("https://www.google.com/")
        print(driver.title)

        # scroll to sport name element
        sport_webelement = driver.find_element_by_xpath(
            "//span[contains(text(), '{}')]".format(sport_name))

        actions = ActionChains(self.driver)
        scroll_bar = driver.find_element_by_css_selector('[class="iScrollIndicator"]:nth-child(1)')
        scrolling_number = (1.1 * scroll_bar.size['height']) * (
                sport_webelement.location['y'] - scroll_bar.location['y']) / (
                                   1000 - scroll_bar.location['y']) - scroll_bar.size['height']
        actions.move_to_element(scroll_bar).click_and_hold() \
            .move_by_offset(0, scrolling_number).perform()

        sport_webelement.click()

        wait = WebDriverWait(driver, 10, poll_frequency=1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[class='liga_menu'] a")))

        tournaments_list = driver. \
            find_elements_by_css_selector("[class='liga_menu'] a")
        for tournament in tournaments_list:
            all_text = tournament.text
            tournament_name = all_text \
                .replace(tournament.find_element_by_css_selector(" span:nth-child(2)").text, "").rstrip()
            tournament_link = tournament.get_attribute("href")
            result.update({tournament_name: tournament_link})

        return result

    def get_games(self, tournament_url: str):
        driver = self.driver
        driver.get(tournament_url)

        tournament_name = driver.find_element_by_css_selector('[class="c-events__liga"]').text
        # get all games in dashboard
        dash_board = driver.find_elements_by_css_selector(
            '[data-name="dashboard-champ-content"] [class="c-events__item c-events__item_col"] [class="c-events__item c-events__item_game"]')

        result = dict()
        game_desctiptions_list = []
        # get each game values
        for game in dash_board:
            coef_names = ['1', 'X', '2', '1X', '12', '2X']
            # get game_date and game_time
            game_date, game_time = game.find_element_by_css_selector('[class="c-events__time-info"] span').text.split(
                ' ')

            # get commands names
            try:
                command_left, command_right = game.find_elements_by_css_selector(
                    '[class="c-events__name"] [class="c-events__team"]')
                command_left = command_left.text
                command_right = command_right.text
            except:
                return dict({tournament_name: "Not valid command names"})
            # get coefs values untill "O"
            game_coefs = []

            coef_elements = game.find_elements_by_css_selector('[class="c-bets"] span')
            for i in range(6):
                game_coefs.append(coef_elements[i].text)

            # locate total button
            total_button = game.find_element_by_css_selector(
                '[class="c-bets"]>span:nth-child(8)')

            try:
                total_button.click()
                total_options_len = len(game.find_elements_by_css_selector('[class="b-markets-dropdown__wrap"] li'))
                total_button.click()
                # get coefs values from "O" to "U" with changing Total
                for i in range(total_options_len):
                    total_button.click()
                    total_options = game.find_elements_by_css_selector('[class="b-markets-dropdown__wrap"] li')
                    coef_names.append('O_TOTAL=' + total_options[i].text)
                    coef_names.append('U_TOTAL=' + total_options[i].text)
                    total_options[i].click()
                    game_coefs.append(coef_elements[6].text)
                    game_coefs.append(coef_elements[8].text)
            except:
                pass
            # dict creation
            game_coefs_dict = dict(zip(coef_names, game_coefs))
            game_desctiption_keys = ["Tournament name", "Left command name", "Right command name",
                                     "Match url", "Coefficients", "Date of Match", "Time of Match"]
            game_desctiption_values = [tournament_name, command_left, command_right,
                                       tournament_url, game_coefs_dict, game_date, game_time]
            game_desctiption = dict(zip(game_desctiption_keys, game_desctiption_values))
            game_desctiptions_list.append(game_desctiption)
        result.update({tournament_name: game_desctiptions_list})
        return result
