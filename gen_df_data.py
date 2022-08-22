import time

import pandas as pd

from src.Cup import Cup
from src.Match import Match
from src.Player import Player
from pprint import PrettyPrinter
import os


def _gen_cup_df(folder: str, year: int):
    if not os.path.exists('data/{}'.format(folder)):
        os.mkdir('data/{}'.format(folder))

    link = 'https://fbref.com/en/comps/1/{0}/schedule/{0}-FIFA-World-Cup-Scores-and-Fixtures'.format(year)
    teams_crawled = []
    # Check for csv and add them to "crawled"
    for file in os.listdir('data/{}'.format(folder)):
        teams_crawled.append(file)

    print('Previously crawled:')
    print(teams_crawled)

    print('Loading World Cup {}'.format(year))
    wc_games = cup.load_cup(link)

    for game in wc_games:
        print('\n')
        print('Loading {} vs. {}'.format(game['home'], game['away']))

        if '{}.csv'.format(game['home']) not in teams_crawled or '{}.csv'.format(game['away']) not in teams_crawled:

            match_players_crawl = match.get_match(game['link'])

            # This does not work for https://fbref.com/en/matches/0a93d0e2/Brazil-Croatia-June-12-2014-FIFA-World-Cup ?
            pp.pprint(match_players_crawl)
            pp.pprint(game)
            exit()
            if '{}.csv'.format(game['home']) not in teams_crawled:
                df_home = _get_match_player(match_players_crawl, 'home', year)
                df_home.to_csv('data/{}/{}.csv'.format(folder, game['home']))
                teams_crawled.append('{}.csv'.format(game['home']))

            if '{}.csv'.format(game['away']) not in teams_crawled:
                df_away = _get_match_player(match_players_crawl, 'away', year)
                df_away.to_csv('data/{}/{}.csv'.format(folder, game['away']))
                teams_crawled.append('{}.csv'.format(game['away']))


def _get_match_player(match_players: dict, team: str, year: int) -> pd.DataFrame:
    df_main = pd.DataFrame(
        columns=['unique_player', 'year', 'player', 'aerial_won_pct', 'complete_pass_pct', 'fouls_per_90',
                 'goalie_save_pct', 'goals_per_90', 'player_type', 'total_matches'])
    df_main.set_index('unique_player')

    for match_player in match_players[team]:
        print('--->Loading {} ({})'.format(match_player['name'], team))
        stats_player_normal = player.get_player_stats(match_player['url_name'], match_player['url_hash'],
                                                      match_player['position'])

        unique_player = match_player['url_name'] + '_' + match_player['url_hash']

        if unique_player not in df_main:
            print('--->--->Saved {} to DF'.format(match_player['name']))
            df_main = pd.concat([df_main, pd.DataFrame.from_records({
                'unique_player': unique_player,
                'year': year,
                'player': match_player['name'],
                'aerial_won_pct': stats_player_normal['aerial_won_pct'],
                'complete_pass_pct': stats_player_normal['complete_pass_pct'],
                'fouls_per_90': stats_player_normal['fouls_per_90'],
                'goalie_save_pct': stats_player_normal['goalie_save_pct'],
                'goals_per_90': stats_player_normal['goals_per_90'],
                'player_type': stats_player_normal['player_type'],
                'total_matches': stats_player_normal['total_matches']
            }, index=[0])])
        else:
            print('--->--->{} already in DF'.format(match_player['name']))

        time.sleep(3)

    return df_main


if __name__ == '__main__':
    pp = PrettyPrinter(indent=4)

    player = Player()
    match = Match()
    cup = Cup()

    # _gen_cup_df('wc18', 2018)
    _gen_cup_df('wc14', 2014)
    _gen_cup_df('wc10', 2010)
    _gen_cup_df('wc06', 2006)
