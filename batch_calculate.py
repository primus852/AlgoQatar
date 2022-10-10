import pandas as pd

from src.Statistic import Poisson
from src.Statistic import Statistic
from src.Visualize import Visualize
from pprint import PrettyPrinter

if __name__ == '__main__':
    pp = PrettyPrinter(indent=4)
    poisson = Poisson()
    stats = Statistic()

    # Build the final DataFrame
    df = stats.create_final_df()

    # Read from CSV
    matches = pd.read_csv('data/matches_groups.csv', sep=',', header=0, index_col='game')

    for index, match in matches.iterrows():
        game = str(index)
        home = str(match['home'])
        away = str(match['away'])

        stats = poisson.calculate(df.loc[home]['lam_cups'], df.loc[away]['lam_cups'], home, away, plot=True)
        vz = Visualize()
        vz.make_markdown_table(home=home, away=away, game=game, stats=stats)
