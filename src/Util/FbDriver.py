from selenium import webdriver
import undetected_chromedriver as uc


class FbDriver:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.__driver = uc.Chrome(executable_path="chrome/chromedriver.exe", chrome_options=options)

    def driver(self) -> uc.Chrome:
        return self.__driver
