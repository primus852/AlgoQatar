import pandas as pd
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By


class Match:

    def __init__(self):

        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.__driver = uc.Chrome(executable_path="chrome/chromedriver.exe", chrome_options=options)

    @staticmethod
    def _get_match_table_type(player_table: pd.DataFrame):
        # Search for "Home Team Player" Table
        if 'Performance' in player_table and 'SCA' in player_table:
            if 'Gls' in player_table['Performance'].iloc[0]:
                return 'players'

    def _get_players(self, player_table: pd.DataFrame) -> list:

        players = []

        for index, row in player_table.iterrows():

            name = row['Unnamed: 0_level_0']['Player']
            pos = row['Unnamed: 2_level_0']['Pos']
            age = str(row['Unnamed: 3_level_0']['Age'])
            minutes = row['Unnamed: 4_level_0']['Min']

            links = self.__driver.find_elements(By.XPATH, '//th/a'.format(name))

            url_name = None
            url_hash = None
            for link_name in links:
                if name == link_name.text:
                    link = link_name.get_attribute('href').split('/')[-2:]
                    url_hash = link[0]
                    url_name = link[1]

            if name.find('Players') > -1:
                break

            players.append({
                'name': name,
                'url_name': url_name,
                'url_hash': url_hash,
                'position': pos,
                'age': age.split('-')[0],
                'minutes_played': minutes
            })

        return players

    def get_match(self, match_link: str):
        df = pd.read_html(match_link)
        self.__driver.get(match_link)

        home = False
        guest = False
        home_players, guest_players = None, None

        for idx, table in enumerate(df):

            table_type = self._get_match_table_type(table)

            if table_type == 'players' and not home:
                home = True
                home_players = self._get_players(table)
                continue

            if table_type == 'players' and not guest:
                guest = True
                guest_players = self._get_players(table)
                continue

        return {
            'home': home_players,
            'guest': guest_players
        }
