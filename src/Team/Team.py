import time
from src.Player import Player
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm
import undetected_chromedriver as uc


class Team:

    def __init__(self, driver: uc.Chrome):
        self.__driver = driver
        self.__player = Player()

    def get_kader_by_year(self, kader_link: str) -> pd.DataFrame:

        df_main = pd.DataFrame(
            columns=['unique_player', 'year', 'player', 'aerial_won_pct', 'complete_pass_pct', 'fouls_per_90',
                     'goalie_save_pct', 'goals_per_90', 'player_type', 'total_matches'])
        df_main.set_index('unique_player')

        self.__driver.get(kader_link)

        player_links = self.__driver.find_elements(By.XPATH, '//table[contains(@id,"stats_standard_1")]'
                                                             '//th[@data-stat="player"]/a')

        idx = 0
        for player in tqdm(player_links, desc='Players'):
            player_pos = self.__driver.find_element(By.XPATH,
                                                    "//tr[@data-row='{}']/td[@data-stat='position']".format(idx)).text

            link = player.get_attribute('href').split('/')[-2:]
            url_hash = link[0]
            url_name = link[1]

            stats_player_normal = self.__player.get_player_stats(url_name, url_hash, player_pos)

            unique_player = url_name + '_' + url_hash

            if unique_player not in df_main:
                df_main = pd.concat([df_main, pd.DataFrame.from_records({
                    'unique_player': unique_player,
                    'player': player.text,
                    'aerial_won_pct': stats_player_normal['aerial_won_pct'],
                    'complete_pass_pct': stats_player_normal['complete_pass_pct'],
                    'fouls_per_90': stats_player_normal['fouls_per_90'],
                    'goalie_save_pct': stats_player_normal['goalie_save_pct'],
                    'goals_per_90': stats_player_normal['goals_per_90'],
                    'player_type': stats_player_normal['player_type'],
                    'total_matches': stats_player_normal['total_matches']
                }, index=[0])])

            idx += 1
            time.sleep(3.5)

        return df_main
