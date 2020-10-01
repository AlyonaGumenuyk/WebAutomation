import re

from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By

from client.pages.base_page import BasePage


class MatchPageLocators:
    SORT_BTN_ROWS = (By.CSS_SELECTOR, '[title="Markets layout"]')
    SORT_BTN_ROWS_1_COL = (By.CSS_SELECTOR, '[title="1 column"]')
    SORT_BTN_EXPAND = (By.CSS_SELECTOR, '[title="Collapse/Expand all"][ class*="nav__btn"]')
    SLIDER_BTN = (By.CSS_SELECTOR, '[class="bet-switch__label active"]')
    TEAMS_TABLO = (By.CSS_SELECTOR, '[class*="c-tablo__team"]')
    SCORE = (By.CSS_SELECTOR, '[class*="c-tablo__main-count"] [class*="c-tablo-count"]')
    TABLO_COEFS = (By.CSS_SELECTOR, '[class="c-chart-stat c-tablo__chart"]')
    BOX_FRAME = (By.CSS_SELECTOR, '#allBetsTable')
    AFTER_GAME_MSG = (By.CSS_SELECTOR, '[class="after-game-info__text"]')
    STATUS_AND_TIMER = (By.CSS_SELECTOR, 'ul[class*="o-tablo-info-list"] [class="c-tablo__text"]')


class MatchPage(BasePage):
    def sort_table(self):
        self.find_element(MatchPageLocators.SORT_BTN_ROWS).click()
        self.find_element(MatchPageLocators.SORT_BTN_ROWS_1_COL).click()
        self.find_element(MatchPageLocators.SORT_BTN_EXPAND).click()
        try:
            sliders = self.find_elements(MatchPageLocators.SLIDER_BTN)
            if sliders:
                for slider in sliders:
                    slider.click()
        except:
            pass
        finally:
            self.find_element(MatchPageLocators.SORT_BTN_EXPAND).click()

    def get_time(self):
        try:
            info = self.find_elements(MatchPageLocators.STATUS_AND_TIMER)
            info_dict = dict()
            status = info[0].text
            time = info[1].text
            info_dict.update({"status": status})
            info_dict.update({"time": time})
            return info_dict
        except:
            return None

    def get_command_names(self):
        try:
            command_names = list(map(lambda x: x.text, self.find_elements(MatchPageLocators.TEAMS_TABLO)))
            return command_names
        except:
            return None

    def get_score(self):
        try:
            score = list(map(lambda x: x.text, self.find_elements(MatchPageLocators.SCORE)))
            return score
        except:
            return None

    def get_dashboard_coefs(self, commands_names):
        try:
            tablo_rows = self.find_elements(MatchPageLocators.TABLO_COEFS)
            tablo_coefs = {"command_left": dict(), "command_right": dict()}
            for row in tablo_rows:
                name_coef = row.find_element_by_css_selector(
                    "[class='c-chart-stat__title']").text
                left_coef = row.find_element_by_css_selector(
                    "[class='c-chart-stat c-tablo__chart'] div:nth-child(2) div:nth-child(1)").text
                right_coef = row.find_element_by_css_selector(
                    "[class='c-chart-stat c-tablo__chart'] div:nth-child(2) div:nth-child(3)").text
                tablo_coefs["command_left"].update({name_coef: left_coef})
                tablo_coefs["command_right"].update({name_coef: right_coef})
            return tablo_coefs
        except:
            return None

    def get_table_coefs(self):
        try:
            table_allcoefs = bs(self.find_element(MatchPageLocators.BOX_FRAME).get_attribute('innerHTML'),
                                features='html.parser')
            table_coefs_dict = dict()
            groups = table_allcoefs.select('div[class="bet_group"]')
            for group in groups:
                group_name = group.find('div', class_=re.compile('.*bet-title.*')).find(text=True,
                                                                                        recursive=False).strip()
                group_coefs = group.select('[class*="bets betCols"] div:not([class*="empty-cell"])')
                group_dict = dict()
                for coef in group_coefs:
                    coef_name = coef.select_one('span:nth-of-type(1)').text.strip()
                    coef_value = coef.select_one('span:nth-of-type(2)').text.strip()
                    group_dict.update({coef_name: coef_value})
                table_coefs_dict.update({group_name: group_dict})
            return table_coefs_dict
        except:
            return None

    def match_is_finished(self):
        try:
            self.driver.find_element_by_css_selector('[class="after-game-info__text"]')
            return True
        except:
            try:
                if self.get_time()["status"] == 'Game finished':
                    return True
            except:
                return False
            return False
