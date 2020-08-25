from selenium import webdriver
import json
import platform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# class TaskQueue(Queue):
#
#
#
# class Worker():
#     def __init__(self, **init_params):
#         self.task_queue = TaskQueue()
#         self.dr 'https://1xstavka.ru/en/line/Football/118587-UEFA-Champions-League/'iver = webdriver.chrome

class Mainer():
    def __init__(self, **init_params):
        if platform.system() == "Windows":
            self.driver = webdriver.Chrome("chromedriver\chromedriver.exe")
        else:
            #self.driver = webdriver.Chrome()
            self.driver = webdriver.Firefox()
        self.driver.set_window_size(1920, 1080)
        self.skills = {"get_tournaments": self.get_tournaments,
                       "get_games": self.get_games}

    def get_tournaments(self, is_line: bool, sport_name: str):
        result = dict()

        driver = self.driver
        if is_line:
            driver.get("https://1xstavka.ru/en/")
        else:
            driver.get("https://1xstavka.ru/live/")

        try:
            wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='sport_menu'] [href='line/Football/']")))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        #wait = ui.WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='liga_menu']")))
        driver.find_element_by_css_selector("[class*='sport_menu'] [href='line/Football/']").click()
        # wait = ui.WebDriverWait(driver, 10)
        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='liga_menu']")))
        # wait.until(driver.fi("[class='liga_menu']"))

        tournaments_list = driver.\
            find_elements_by_css_selector("[class='liga_menu'] a")
        print(len(tournaments_list))
        for tournament in tournaments_list:
            all_text = tournament.text
            tournament_name = all_text \
                .replace(tournament.find_element_by_css_selector(" span:nth-child(2)").text, "").rstrip()
            tournament_link = tournament.get_attribute("href")
            result.update({tournament_name: tournament_link})

        return json.dumps(result)

    def get_games(self, is_line: bool, tournament_url: str):
        driver = self.driver
        driver.get(tournament_url)

        name_coeff_elem = driver. \
            find_element_by_css_selector(
            '[data-name="dashboard-champ-content"] [class="c-events__item c-events__item_head blueBack"] [class="c-bets"]').text
        name_coeff = name_coeff_elem.split('\n')
        dictionary_of_coef = dict()
        for name in name_coeff:
            dictionary_of_coef.update({name: ''})

        dash_board = driver. \
            find_elements_by_css_selector(
            '[data-name="dashboard-champ-content"] [class="c-events__item c-events__item_col"] [class="c-events__item c-events__item_game"]')

        for game in dash_board:
            date, time = game.find_element_by_css_selector('[class="c-events__time-info"]').text.split(' ')

            command_left, command_right = game.find_elements_by_css_selector(
                '[class="c-events__name"] [class="c-events__team"]')
            command_left = command_left.text
            command_right = command_right.text

            coef_elements = game.find_elements_by_css_selector('[class="c-bets"]')


mainer = Mainer()
try:
    print(mainer.get_tournaments(True, 'Football'))
finally:
    mainer.driver.close()
