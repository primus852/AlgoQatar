import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By


class Cup:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.__driver = uc.Chrome(executable_path="chrome/chromedriver.exe", chrome_options=options)

    def load_cup(self, url: str):

        self.__driver.get(url)

        matches_in_cup = []

        rows = self.__driver.find_elements(By.XPATH, "//tr[@data-row]")

        for row in rows:

            tds = row.find_elements(By.TAG_NAME, "td")
            home_team = None
            away_team = None
            match_link = None

            for col in tds:
                stat = col.get_attribute('data-stat')

                if stat == 'home_team':
                    if col.text != "":
                        home_team_elem = col.find_element(By.TAG_NAME, "a")
                        if home_team_elem:
                            home_team = home_team_elem.text

                if stat == 'away_team':
                    if col.text != "":
                        away_team_elem = col.find_element(By.TAG_NAME, "a")
                        if away_team_elem:
                            away_team = away_team_elem.text

                if stat == 'match_report':
                    if col.text != "":
                        match_link_elem = col.find_element(By.TAG_NAME, "a")
                        if match_link_elem:
                            match_link = match_link_elem.get_attribute('href')

            if away_team is not None and home_team is not None and match_link is not None:
                matches_in_cup.append({
                    'home': home_team,
                    'away': away_team,
                    'link': match_link
                })

        return matches_in_cup
