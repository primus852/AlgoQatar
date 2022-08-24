from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import os


class Util:

    @staticmethod
    def setup_chrome() -> uc.Chrome:
        """
        Init the Chrome Driver to pass to classes
        Also click the cookie banner to make ads show
        """
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = uc.Chrome(executable_path="chrome/chromedriver.exe", chrome_options=options)

        driver.get('https://fbref.com/en/')
        time.sleep(2)
        agree_button = driver.find_element(By.XPATH, "//button[contains(text(),'AGREE')]")
        agree_button.click()

        return driver

    @staticmethod
    def load_teams_from_files(keep_ending=True) -> list:

        teams = []

        folders = [dI for dI in os.listdir('data') if os.path.isdir(os.path.join('data', dI))]
        for folder in folders:
            for file in os.listdir('data/{}/teams'.format(folder)):
                if keep_ending:
                    teams.append(file)
                else:
                    teams.append(file.replace('.csv', ''))

        return teams
