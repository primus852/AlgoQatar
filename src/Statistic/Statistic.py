from src.Util import Util
import pandas as pd


class Statistic:

    def create_final_df(self) -> pd.DataFrame:

        # Collect all Games
        df_games = Util.merge_games_to_df()

        # Final DF
        df = pd.DataFrame(columns=['team', 'lam_cups', 'lam_players']).set_index('team')

        # List of Teams
        teams = Util.load_teams_from_current(keep_ending=False)

        i = 0
        for team in teams:
            stats = self.__get_team_stats(team, df_games)
            df = pd.concat([df, pd.DataFrame.from_records(stats, index=[0]).set_index('team')])
            i += 1

        # Fill missing lam values
        df['lam_cups'] = df['lam_cups'].fillna(0)

        # Enrich with lam calculated by players
        for team_stats in df.iterrows():
            df.loc[team_stats[0], 'lam_players'] = self.__get_players_by_team(str(team_stats[0]))

        return df

    @staticmethod
    def __get_team_stats(team: str, df_games: pd.DataFrame) -> dict:
        df_team_home = df_games.loc[df_games['home'] == team, 'score_home']
        df_team_away = df_games.loc[df_games['away'] == team, 'score_away']

        lam_team = (df_team_home.mean() + df_team_away.mean()) / 2

        return {
            'team': team,
            'lam_cups': lam_team,
            'lam_players': 0
        }

    @staticmethod
    def __get_players_by_team(team: str) -> float:
        df = Util.load_players_by_team(team)

        return df['goals_per_90'].mean()
