import json
import time

from flask import Response
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from client.worker import Worker


class Mainer(Worker):
    def __init__(self, task_queue):
        super().__init__(task_queue)
        self.skills = {"get_tournaments": self.get_tournaments,
                       "get_games": self.get_games}

    @staticmethod
    def get_new_tasks():
        time_to_sleep = 10
        print("sleeping for {} seconds while waiting for tasks".format(time_to_sleep))
        time.sleep(time_to_sleep)

    def work(self):
        if self.task_queue.empty():
            self.get_new_tasks()
        task = self.task_queue.get()
        report = self.do_task(task)
        print(report)

    def do_task(self, task):
        if task.method == 'get_tournaments':
            result = self.get_tournaments(task.params[0], task.params[1])
            try:
                with open('task_report/tournaments.json', 'w') as current_tournaments:
                    json.dump(result, current_tournaments, indent=4)
                return Response(status=200)
            except FileNotFoundError:
                return Response("'task_report/tournaments.json', something went wrong", status=404)
        elif task.method == 'get_games':
            result = self.get_games(task.params[0], task.params[1])
            try:
                with open('task_report/games.json', 'a') as current_games:
                    json.dump(result, current_games, indent=4)
                    current_games.write('\n')
                return Response(status=200)
            except FileNotFoundError:
                return Response("'task_report/games.json', something went wrong", status=404)

    def do_work(self):
        while True:
            self.work()

    def get_tournaments(self, is_line: bool, sport_name: str):
        result = dict()

        driver = self.driver
        if is_line:
            driver.get("https://1xstavka.ru/line/")
            line_or_live = "line"
        else:
            driver.get("https://1xstavka.ru/live/")
            line_or_live = "live"

        try:
            wait = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='sport_menu'] [href='{}/{}/']"
                                                .format(line_or_live, sport_name))))
            # print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        driver.find_element_by_css_selector("[class*='sport_menu'] [href='{}/{}/']"
                                            .format(line_or_live, sport_name)).click()

        wait = WebDriverWait(driver, 10, poll_frequency=1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[class='liga_menu'] a")))

        tournaments_list = driver. \
            find_elements_by_css_selector("[class='liga_menu'] a")
        # print(len(tournaments_list))
        for tournament in tournaments_list:
            all_text = tournament.text
            tournament_name = all_text \
                .replace(tournament.find_element_by_css_selector(" span:nth-child(2)").text, "").rstrip()
            tournament_link = tournament.get_attribute("href")
            result.update({tournament_name: tournament_link})

        # print(result)

        return result

    def get_games(self, is_line: bool, tournament_url: str):
        driver = self.driver
        driver.get(tournament_url)

        # print(coef_names)

        tournament_name = driver.find_element_by_css_selector('[class="c-events__liga"]').text
        # get all games in dashboard
        dash_board = driver.find_elements_by_css_selector(
            '[data-name="dashboard-champ-content"] [class="c-events__item c-events__item_col"] [class="c-events__item c-events__item_game"]')

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
                return json.dumps(dict({tournament_name: "Not valid command names"}))
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

        game_json = json.dumps(game_desctiptions_list)
        return game_json
