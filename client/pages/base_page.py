import json
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePageLocators:
    SPORT_NAME = (By.XPATH, '//span[contains(text(), "{}")]')
    TOURNAMENTS = (By.CSS_SELECTOR, '[class="liga_menu"] a')
    OUR_TOURNAMENT = (By.XPATH, '//ul[@class="liga_menu"] //a[normalize-space(text()) = "{}"]')
    GAMES = (By.CSS_SELECTOR, '[class="event_menu"] a')
    GAME_STAT = (By.CSS_SELECTOR, '[class="c-events main_game"]')


class BasePage:
    def __init__(self, driver, better):
        self.driver = driver
        self.better = better

    def go_to_match(self, params):
        self.driver.get('https://1xstavka.ru/en/live/')
        sport_name = (BasePageLocators.SPORT_NAME[0], BasePageLocators.SPORT_NAME[1].format('Football'))
        sport_webelement = self.find_elements(sport_name)[0]

        # scroll to element and wait for drop down to show
        self.better.scroll_to_element(sport_webelement)
        sport_webelement.click()
        self.find_element(BasePageLocators.TOURNAMENTS)

        # open tournament
        our_tournament = (BasePageLocators.OUR_TOURNAMENT[0],
                          BasePageLocators.OUR_TOURNAMENT[1].format(params[1]))
        try:
            tournament_el = self.find_element(our_tournament, time_to_wait=600)
        except:
            raise Exception('No tournament with such name')

        try:
            tournament_el.click()
        except:
            self.better.scroll_to_element(tournament_el)
            tournament_el.click()

        # find the game
        games_list_el = self.find_elements(BasePageLocators.GAMES)
        match_link = None
        tries_to_find_match = 0
        while tries_to_find_match < 60:
            for game_el in games_list_el:
                command_names = game_el.find_elements_by_css_selector('div[class="ls-game__name"]')
                left_command = command_names[0].text
                right_command = command_names[1].text
                if left_command == params[2] and right_command == params[3]:
                    match_link = command_names[0]
            if match_link:
                break
            else:
                tries_to_find_match += 1
                if tries_to_find_match >= 59:
                    raise Exception('No match with such command names')
                time.sleep(10)

        try:
            match_link.click()
        except:
            self.better.scroll_to_element(match_link, force_scroll=True)
            match_link.click()

        self.find_element(BasePageLocators.GAME_STAT)

    def close_page(self):
        self.driver.close()

    def freeze_page(self):
        self.driver.execute_script(
            "window.oldjQuery=window.jQuery;delete window.jQuery;delete "
            "window.$;window.oSend=XMLHttpRequest.prototype.send;XMLHttpRequest.prototype.send = function(){"
            "console.log('stopped ajax request', arguments)};")

    def unfreeze_page(self):
        self.driver.execute_script(
            "window.jQuery=window.oldjQuery;window.$=window.jQuery;XMLHttpRequest.prototype.send=window.oSend")

    def find_element(self, locator, time_to_wait=5):
        return WebDriverWait(self.driver, time_to_wait).until(EC.presence_of_element_located(locator),
                                                              message=json.dumps(
                                                                  {
                                                                      "Error": f"Can't find element by locator {locator}"}))

    def find_elements(self, locator, time_to_wait=5):
        return WebDriverWait(self.driver, time_to_wait).until(EC.presence_of_all_elements_located(locator),
                                                              message=json.dumps(
                                                                  {
                                                                      "Error": f"Can't find elements by locator {locator}"}))
