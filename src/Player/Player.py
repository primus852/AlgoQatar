import pandas as pd


class Player:

    def get_player_stats(self, player: str, hash_id: str, player_type: str) -> dict:

        try:
            df = pd.read_html('https://fbref.com/en/players/{}/nat_tm/{}-National-Team-Stats'.format(hash_id, player))
        except:
            return {
                'total_matches': 0,
                'goals_per_90': 0,
                'complete_pass_pct': 0,
                'progessive_pass_distance': 0,
                'aerial_won_pct': 0,
                'fouls_per_90': 0,
                'goalie_save_pct': 0,
                'player_type': player_type
            }

        total_matches, goals_per_90 = None, None
        complete_pass_pct, progressive_pass_distance = None, None
        aerial_won_pct, fouls_per_90 = None, None
        save_pct = None

        for idx, table in enumerate(df):

            table_type = self._get_player_table_type(table)

            if table_type == 'standard':
                total_matches, goals_per_90 = self._get_player_standard(table)
                continue

            if table_type == 'passing':
                complete_pass_pct, progressive_pass_distance = self._get_player_passing(table)
                continue

            if table_type == 'misc':
                aerial_won_pct, fouls_per_90 = self._get_player_misc(table, total_matches)
                continue

            if table_type == 'goalie':
                save_pct = self._get_player_goalie(table)
                continue

        return {
            'total_matches': total_matches,
            'goals_per_90': goals_per_90,
            'complete_pass_pct': complete_pass_pct,
            'progessive_pass_distance': progressive_pass_distance,
            'aerial_won_pct': aerial_won_pct,
            'fouls_per_90': fouls_per_90,
            'goalie_save_pct': save_pct,
            'player_type': player_type
        }

    @staticmethod
    def _get_player_table_type(player_table: pd.DataFrame):
        # Search for "Standard Stats" Table
        if 'Playing Time' in player_table and 'Performance' in player_table and 'Per 90 Minutes' in player_table:
            if 'MP' in player_table['Playing Time'].iloc[0]:
                return 'standard'

            # Different Table Layouts?!? See Fyodor Smolov and Roman Zobnin for example
            if 'Unnamed: 5_level_0' in player_table:
                if 'MP' in player_table['Unnamed: 5_level_0'].iloc[0]:
                    return 'standard'

        # Search for "Passes" Table
        if 'Total' in player_table and 'Short' in player_table:
            if 'Cmp%' in player_table['Total'].iloc[0]:
                return 'passing'

        # Search for "Shooting" Table
        if 'Standard' in player_table:
            if 'SoT%' in player_table['Standard'].iloc[0]:
                return 'shooting'

        # Search for "Misc" Table
        if 'Performance' in player_table:
            if 'Recov' in player_table['Performance'].iloc[0]:
                return 'misc'

        # Search for "Goalkeeping" Table
        if 'Performance' in player_table:
            if 'Save%' in player_table['Performance'].iloc[0]:
                return 'goalie'

    @staticmethod
    def _get_summary_index(pt: pd.DataFrame) -> int:
        # Get the row with Summary Stats
        summary_index = None

        for index, row in pt['Unnamed: 0_level_0'].iterrows():
            # Check if row includes "Seasons" for the first time, take it and exit

            if str(row['Season']).find('Season') > -1:
                summary_index = index
                break

        return summary_index

    def _get_player_passing(self, player_table: pd.DataFrame) -> tuple:
        summary_index = self._get_summary_index(player_table)

        passes_completed = player_table['Total'].iloc[summary_index]['Cmp%']

        if float(player_table['Total'].iloc[summary_index]['Cmp']) > 0:
            passes_progressive_distance = round(
                float(player_table['Total'].iloc[summary_index]['PrgDist']) /
                float(player_table['Total'].iloc[summary_index]['Cmp']), 0)
        else:
            passes_progressive_distance = float(0)

        return passes_completed, passes_progressive_distance

    def _get_player_misc(self, player_table: pd.DataFrame, matches: int) -> tuple:
        if matches is None:
            print('No Matches found, wrong table order?')
            exit()

        summary_index = self._get_summary_index(player_table)

        aerial_duels_won_pct = float(player_table['Aerial Duels'].iloc[summary_index]['Won%'])
        fouls_committed_90 = round(float(player_table['Performance'].iloc[summary_index]['Fls']) / matches, 2)

        return aerial_duels_won_pct, fouls_committed_90

    def _get_player_goalie(self, player_table: pd.DataFrame) -> float:

        summary_index = self._get_summary_index(player_table)

        shots_saved = float(player_table['Performance'].iloc[summary_index]['Save%'])

        return shots_saved

    def _get_player_standard(self, player_table: pd.DataFrame) -> tuple:
        summary_index = self._get_summary_index(player_table)

        if 'Unnamed: 5_level_0' in player_table:
            matches_played = int(player_table['Unnamed: 5_level_0'].iloc[summary_index]['MP'])
        else:
            matches_played = int(player_table['Playing Time'].iloc[summary_index]['MP'])

        goals_per_90 = float(player_table['Per 90 Minutes'].iloc[summary_index]['Gls'])

        return matches_played, goals_per_90
