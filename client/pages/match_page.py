from selenium.webdriver import ActionChains
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
    BOX_FRAME = (By.CSS_SELECTOR, '[class="bets_content betsscroll"]')
    TABLE_GROUPS = (By.CSS_SELECTOR, '[class="bet_group"]')
    TABLE_GROUP_NAME = '[class*="bet-title"]'
    TABLE_GROUP_COEFS = '[class*="bets betCols"] div:not([class*="empty-cell"])'
    TABLE_GROUP_COEFS_NAMES = 'span:nth-child(1)'
    TABLE_GROUP_COEFS_VALUES = 'span:nth-child(2)'


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

    def get_command_names(self):
        return list(map(lambda x: x.text, self.find_elements(MatchPageLocators.TEAMS_TABLO)))

    def get_score(self):
        return list(map(lambda x: x.text, self.find_elements(MatchPageLocators.SCORE)))

    def get_dashboard_coefs(self, commands_names):
        tablo_rows = self.find_elements(MatchPageLocators.TABLO_COEFS)
        if tablo_rows:
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
        else:
            tablo_coefs = None
        return tablo_coefs

    def get_table_coefs(self):
        self.freeze_page()
        group_coefs_list = self.find_elements(MatchPageLocators.TABLE_GROUPS)
        table_coefs_dict = dict()
        for group in group_coefs_list:
            group_name = group.find_element_by_css_selector(MatchPageLocators.TABLE_GROUP_NAME).text
            if not group_name:
                self.driver.execute_script("arguments[0].scrollIntoView(false);", group)
                group_name = group.find_element_by_css_selector(MatchPageLocators.TABLE_GROUP_NAME).text
            coefs_in_group = group.find_elements_by_css_selector(MatchPageLocators.TABLE_GROUP_COEFS)
            coefs_in_group_dict = dict()
            for coef in coefs_in_group:
                coef_name = coef.find_element_by_css_selector(MatchPageLocators.TABLE_GROUP_COEFS_NAMES).text
                coef_value = coef.find_element_by_css_selector(MatchPageLocators.TABLE_GROUP_COEFS_VALUES).text
                if not coef_name:
                    self.driver.execute_script("arguments[0].scrollIntoView(false);", coef)
                    coef_name = coef.find_element_by_css_selector(MatchPageLocators.TABLE_GROUP_COEFS_NAMES).text
                    coef_value = coef.find_element_by_css_selector(MatchPageLocators.TABLE_GROUP_COEFS_VALUES).text
                coefs_in_group_dict.update({coef_name: coef_value})
            table_coefs_dict.update({group_name: coefs_in_group_dict})
        self.unfreeze_page()

        return table_coefs_dict
