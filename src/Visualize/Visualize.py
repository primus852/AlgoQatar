import pandas as pd
from markdownTable import markdownTable


class Visualize:

    @staticmethod
    def make_markdown_table(home: str, away: str, game: str | int, stats: dict):

        # Probabilities
        prob = [
            'Win: {}%'.format(round(stats['outcome']['win_home'] * 100, 0)),
            'Lose: {}%'.format(round(stats['outcome']['lose_home'] * 100, 0)),
            'Tie: {}%'.format(round(stats['outcome']['tie'] * 100, 0))
        ]

        scores_home = []
        # Append to home if exists
        for i in range(3):
            try:
                scores_home.append(
                    '{}: {} Goal(s)'.format(list(stats['home']['top3'].keys())[i],
                                            stats['home']['top3'][list(stats['home']['top3'].keys())[i]]),
                )
            except IndexError:
                pass

        scores_away = []
        # Append to away if exists
        for i in range(3):
            try:
                scores_away.append(
                    '{}: {} Goal(s)'.format(list(stats['away']['top3'].keys())[i],
                                            stats['away']['top3'][list(stats['away']['top3'].keys())[i]]),
                )
            except IndexError:
                pass

        poss_results = []
        # Append to Scores if exists
        idx = 0
        for _ in stats['scores']:
            result_key = list(stats['scores'][idx].keys())[0]
            result_value = stats['scores'][idx][result_key]
            poss_results.append('{}: {}'.format(result_key, result_value))
            idx += 1

        data = [
            [
                '<br />'.join(prob),
                '<br />'.join(scores_home),
                '<br />'.join(scores_away),
                '<br />'.join(poss_results)]
        ]

        df = pd.DataFrame(data,
                          columns=['Probablities {}'.format(home), 'Top 3 Scores - {}'.format(home),
                                   'Top 3 Scores - {}'.format(away), 'Possible Results'])

        print('')
        print('## {} - {} vs. {}'.format(game, home, away))
        print(markdownTable(df.to_dict(orient='records')).setParams(row_sep='markdown', quote=False).getMarkdown())
