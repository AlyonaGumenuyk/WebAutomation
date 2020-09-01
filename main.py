import json
import platform

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import constants



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
            # self.driver = webdriver.Chrome()
            self.driver = webdriver.Firefox()
        self.driver.set_window_size(1920, 1080)
        self.skills = {"get_tournaments": self.get_tournaments,
                       "get_games": self.get_games}

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
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        driver.find_element_by_css_selector("[class*='sport_menu'] [href='{}/{}/']"
                                            .format(line_or_live, sport_name)).click()

        wait = WebDriverWait(driver, 10, poll_frequency=1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[class='liga_menu'] a")))

        tournaments_list = driver. \
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

        coef_names = constants.COEF_NAMES
        print(coef_names)

        # get all games in dashboard
        dash_board = driver. \
            find_elements_by_css_selector(
            '[data-name="dashboard-champ-content"] [class="c-events__item c-events__item_col"] [class="c-events__item c-events__item_game"]')

        # get each game values
        for game in dash_board:

            # get date and time
            date, time = game.find_element_by_css_selector('[class="c-events__time-info"]').text.split(' ')

            # get commands names
            command_left, command_right = game.find_elements_by_css_selector(
                '[class="c-events__name"] [class="c-events__team"]')
            command_left = command_left.text
            command_right = command_right.text

            # get coefs values untill "O"
            game_coefs = []
            coef_elements = game.find_elements_by_css_selector('[class="c-bets"] a')
            for i in range(6):
                game_coefs.append(coef_elements[i].text)

            # locate total button
            total_button = game.find_element_by_css_selector(
                '[class="c-bets__bet non num c-bets__bet_sm static-event"]')

            # get coefs values from "O" to "U" with changing Total
            for i in range(5):
                total_button.click()
                total_options = game.find_elements_by_css_selector('[class="b-markets-dropdown__wrap"] li')
                total_options[i].click()
                game_coefs.append(coef_elements[6].text)
                game_coefs.append(coef_elements[8].text)

            # dict creation
            game_coefs_dict = dict(zip(coef_names, game_coefs))
            game_desctiption_keys = ["Left command name", "Right command name",
                                     "Match url", "Coefficients", "Date of Match", "Time of Match"]
            game_desctiption_values = [command_left, command_right,
                                       tournament_url, game_coefs_dict, date, time]
            game_desctiption = dict(zip(game_desctiption_keys, game_desctiption_values))
            game_json = json.dumps(game_desctiption)

        return json.dumps(game_desctiption)


class Better():
    def __init__(self, **init_params):
        if platform.system() == "Windows":
            self.driver = webdriver.Chrome("chromedriver\chromedriver.exe")
        else:
            # self.driver = webdriver.Chrome()
            self.driver = webdriver.Firefox()
        self.driver.set_window_size(1920, 1080)
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
        total_cells = driver.find_elements_by_xpath("//*[normalize-space(text()) = 'Total']/../div[@class='bets "
                                                    "betCols2']/div")
        coefs = dict()
        for cell in total_cells:
            coef_name = cell.find_element_by_css_selector("[class = 'bet_type']").text
            coef_value = cell.find_element_by_css_selector("[class = 'koeff']").text
            coefs.update({coef_name: coef_value})

        return json.dumps(coefs)

    def make_bet(self):
        return 0


#mainer = Mainer()
#better = Better()
try:
    #print(constants.COEF_NAMES)
    print(1)
    # print(mainer.get_games(True, "https://1xstavka.ru/en/line/Football/1706694-UEFA-Nations-League/"))
    # mainer.login("mrwithoutnickname@gmail.com", "h6E-qYg-FDR-7b8")
    #print(better.get_coefs("https://1xstavka.ru/en/live/Tennis/2130892-US-Open-2020/254093666-Vasek-Pospisil-Philipp-Kohlschreiber/"))
finally:
    print("123")
    #mainer.driver.close()
    #better.driver.close()
