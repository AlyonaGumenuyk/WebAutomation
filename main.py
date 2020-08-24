from selenium import webdriver
import json

# class TaskQueue(Queue):
#
#
#
# class Worker():
#     def __init__(self, **init_params):
#         self.task_queue = TaskQueue()
#         self.driver = webdriver.chrome

class Mainer():
    def __init__(self, **init_params):
        self.driver = webdriver.Chrome("chromedriver/chromedriver.exe")
        self.driver.set_window_size(1920, 1080)
        self.skills = {"get_tournaments": self.get_tournaments,
                       "get_games": self.get_games}

    def get_tournaments(self, is_line:bool):
        result = dict()

        driver = self.driver
        if is_line:
            driver.get("https://1xstavka.ru/line/Football/")
        else:
            driver.get("https://1xstavka.ru/live/Football/")

        tournaments_list = driver. \
            find_elements_by_css_selector("[class='liga_menu'] a")
        print(len(tournaments_list))
        for tournament in tournaments_list:
            all_text = tournament.text
            tournament_name = all_text\
                .replace(tournament.find_element_by_css_selector(" span:nth-child(2)").text, "").rstrip()
            tournament_link = tournament.get_attribute("href")
            result.update({tournament_name:tournament_link})

        return json.dumps(result)

        # for tournament in tournaments_list:
        #     tournament_name = tournament.find_element_by_css_selector('[class="c-events__liga"]').text
        #     tournaments_dictionary.update({tournament_name: dict()})
        #     # print(tournament_name)
        #     games_list = tournament.find_elements_by_css_selector('[class="c-events__item c-events__item_col"]')
        #     match_number = 1
        #     for game in games_list:
        #         command_list = game.find_elements_by_css_selector('[class="c-events__team"]')
        #         tournaments_dictionary[tournament_name].update({'match#' + str(match_number): dict()})
        #         tournaments_dictionary[tournament_name]['match#' + str(match_number)].update(
        #             zip(['command_left', 'command_right'], [command_list[0].text, command_list[1].text]))
        #         match_number += 1
        #         # print(list(map(lambda x: x.text, command_list)))
        # print(tournaments_dictionary)

    def get_games(self, is_line:bool, tournament_url:str):
        driver = self.driver
        driver.get(tournament_url)

        name_coeff_elem = driver.\
            find_element_by_css_selector('[data-name="dashboard-champ-content"] [class="c-events__item c-events__item_head blueBack"] [class="c-bets"]').text
        name_coeff = name_coeff_elem.split('\n')
        dictionary_of_coef = dict()
        for name in name_coeff:
            dictionary_of_coef.update({name:''})

        dash_board = driver.\
            find_elements_by_css_selector('[data-name="dashboard-champ-content"] [class="c-events__item c-events__item_col"] [class="c-events__item c-events__item_game"]')

        for game in dash_board:
            date, time = game.find_element_by_css_selector('[class="c-events__time-info"]').text.split(' ')

            command_left, command_right = game.find_elements_by_css_selector('[class="c-events__name"] [class="c-events__team"]')
            command_left = command_left.text
            command_right = command_right.text

            coef_elements = game.find_elements_by_css_selector('[class="c-bets"]')










mainer = Mainer()
mainer.get_games(True, 'https://1xstavka.ru/en/line/Football/118587-UEFA-Champions-League/')

mainer.driver.close()
