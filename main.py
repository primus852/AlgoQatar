from src.Cup import Cup
from src.Match import Match
from src.Player import Player
from pprint import PrettyPrinter

if __name__ == '__main__':
    pp = PrettyPrinter(indent=4)

    player = Player()
    match = Match()
    cup = Cup()

    wc18_games = cup.load_cup('https://fbref.com/en/comps/1/2018/schedule/2018-FIFA-World-Cup-Scores-and-Fixtures')

    for game in wc18_games:
        match_players = match.get_match(game['link'])

        for match_player in match_players['home']:
            stats_player_normal = player.get_player_stats(match_player['url_name'], match_player['url_hash'],
                                                          match_player['position'])
            print(stats_player_normal)
            exit()

    # match_players = match.get_match('Russia-Saudi-Arabia-June-14-2018-FIFA-World-Cup', 'c9d7e48c')

    # stats_player_normal = player.get_player_stats('Alan-Dzagoev', '4c45cdc2', 'FW')
    # stats_player_goalie = player.get_player_stats('Igor-Akinfeev', '42ec696a', 'GK')
    # print(stats_player_normal)
    # print(stats_player_goalie)
