from selenium.webdriver.common.by import By
from src.Player import Player
from src.Util import Util
from src.Match import Match
from src.Team import Team

import pandas as pd
import os
import undetected_chromedriver as uc


class Cup:

    def __init__(self, driver: uc.Chrome):

        self.__driver = driver
        self.__player = Player()
        self.__match = Match(self.__driver)
        self.__team = Team(self.__driver)

    def crawl_missing_df(self):

        if not os.path.exists('data/wcCurrent'):
            os.mkdir('data/wcCurrent')

        if not os.path.exists('data/wcCurrent/teams'):
            os.mkdir('data/wcCurrent/teams')

        teams_crawled = []
        # Check for csv and add them to "crawled"
        for file in os.listdir('data/wcCurrent/teams'):
            teams_crawled.append(file)

        teams = self.__load_current_cup()
        missing_teams = []

        all_teams = Util.load_teams_from_files(keep_ending=False)

        for team in teams:
            if team['team'] not in all_teams:
                missing_teams.append(team)

        for missing_team in missing_teams:
            kader = self.__team.get_kader_by_year(missing_team['link'])
            kader.to_csv('data/wcCurrent/{}.csv'.format(missing_team['team']))
            teams_crawled.append('{}.csv'.format(missing_team['team']))

    def crawl_cup_df(self, year: int, games_in_cup: int = 64) -> None:
        folder_teams = 'wc{}/teams'.format(year)
        folder_games = 'wc{}/games'.format(year)

        if not os.path.exists('data/wc{}'.format(year)):
            os.mkdir('data/wc{}'.format(year))

        if not os.path.exists('data/{}'.format(folder_teams)):
            os.mkdir('data/{}'.format(folder_teams))

        if not os.path.exists('data/{}'.format(folder_games)):
            os.mkdir('data/{}'.format(folder_games))

        link = 'https://fbref.com/en/comps/1/{0}/schedule/{0}-FIFA-World-Cup-Scores-and-Fixtures'.format(year)

        teams_crawled = []
        # Check for csv and add them to "crawled"
        for file in os.listdir('data/{}'.format(folder_teams)):
            teams_crawled.append(file)

        print('Previously crawled Teams:')
        print(teams_crawled)

        games_crawled = []
        # Check for csv and add them to "crawled"
        for file in os.listdir('data/{}'.format(folder_games)):
            games_crawled.append(file)

        print('Previously crawled Games:')
        print(games_crawled)

        # Count games and see if we have the right amount already
        if len(games_crawled) == games_in_cup:
            print('Crawling is done already')
            return

        print('Loading World Cup {}'.format(year))
        wc_games = self.__load_historic_cup(link)

        game_count = 1
        for game in wc_games:
            print('Loading {} vs. {}'.format(game['home'], game['away']))

            if '{}.csv'.format(game['home']) not in teams_crawled or '{}.csv'.format(
                    game['away']) not in teams_crawled or 'game_{}.csv'.format(game_count) not in games_crawled:

                print('Crawling Match...')

                if '{}.csv'.format(game['home']) not in teams_crawled:
                    print(game['home'])
                    kader_home = self.__team.get_kader_by_year(game['home_link'])
                    kader_home.to_csv('data/{}/{}.csv'.format(folder_teams, game['home']))
                    teams_crawled.append('{}.csv'.format(game['home']))
                else:
                    print('{} already crawled'.format(game['home']))

                if '{}.csv'.format(game['away']) not in teams_crawled:
                    print(game['away'])
                    kader_away = self.__team.get_kader_by_year(game['away_link'])
                    kader_away.to_csv('data/{}/{}.csv'.format(folder_teams, game['away']))
                    teams_crawled.append('{}.csv'.format(game['away']))
                else:
                    print('{} already crawled'.format(game['away']))

                if 'game_{}.csv'.format(game_count) not in games_crawled:
                    match_players_crawl = self.__match.get_match(game['link'])
                    game_info = {
                        'home': game['home'],
                        'away': game['away'],
                        'score_home': match_players_crawl['score']['home'],
                        'score_away': match_players_crawl['score']['away'],
                    }

                    df_game = pd.DataFrame(game_info, index=[0])

                    df_game.to_csv('data/{}/game_{}.csv'.format(folder_games, game_count))
                else:
                    print('Game {} already crawled'.format(game_count))

            else:
                print('Home, Away and Game already crawled, skipping...')

            game_count += 1

    def __load_current_cup(self) -> list:
        self.__driver.get('https://fbref.com/en/comps/1/FIFA-World-Cup-Stats')

        rows = self.__driver.find_elements(By.XPATH, "//td[@data-stat='team']/a")

        participants = []
        for row in rows:
            participants.append({
                'link': row.get_attribute('href'),
                'team': row.text
            })

        return participants

    def __load_historic_cup(self, url: str):

        self.__driver.get(url)

        matches_in_cup = []

        rows = self.__driver.find_elements(By.XPATH, "//tr[@data-row]")

        for row in rows:

            tds = row.find_elements(By.TAG_NAME, "td")
            home_team = None
            home_team_link = None
            away_team = None
            away_team_link = None
            match_link = None

            for col in tds:
                stat = col.get_attribute('data-stat')

                if stat == 'home_team':
                    if col.text != "":
                        home_team_elem = col.find_element(By.TAG_NAME, "a")
                        if home_team_elem:
                            home_team = home_team_elem.text
                            home_team_link = home_team_elem.get_attribute('href')

                if stat == 'away_team':
                    if col.text != "":
                        away_team_elem = col.find_element(By.TAG_NAME, "a")
                        if away_team_elem:
                            away_team = away_team_elem.text
                            away_team_link = away_team_elem.get_attribute('href')

                if stat == 'match_report':
                    if col.text != "":
                        match_link_elem = col.find_element(By.TAG_NAME, "a")
                        if match_link_elem:
                            match_link = match_link_elem.get_attribute('href')

            if away_team is not None and home_team is not None and match_link is not None:
                matches_in_cup.append({
                    'home': home_team,
                    'home_link': home_team_link,
                    'away': away_team,
                    'away_link': away_team_link,
                    'link': match_link
                })

        return matches_in_cup
