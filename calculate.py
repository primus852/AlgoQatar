from src.Statistic import Poisson
from src.Statistic import Statistic
from pprint import PrettyPrinter

if __name__ == '__main__':
    pp = PrettyPrinter(indent=4)
    poisson = Poisson()
    stats = Statistic()

    # Build the final DataFrame
    df = stats.create_final_df()

    home = 'Qatar'
    away = 'Ecuador'

    stats = poisson.calculate(df.loc[home]['lam_cups'], df.loc[away]['lam_cups'], home, away, plot=True)

    print('************RESULTS************')

    print('Probabilities:')
    print('\t{}:'.format(home))
    print('\t\tWin: {}%'.format(round(stats['outcome']['win_home'] * 100, 0)))
    print('\t\tLose: {}%'.format(round(stats['outcome']['lose_home'] * 100, 0)))
    print('\t\tTie: {}%'.format(round(stats['outcome']['tie'] * 100, 0)))

    print('-------------------')

    print('Top 3 Scores:')
    print('\t{}:'.format(home))
    print('\t\t{}: {} Goal(s)'.format(list(stats['home']['top3'].keys())[0],
                                      stats['home']['top3'][list(stats['home']['top3'].keys())[0]]))
    print('\t\t{}: {} Goal(s)'.format(list(stats['home']['top3'].keys())[1],
                                      stats['home']['top3'][list(stats['home']['top3'].keys())[1]]))
    try:
        print('\t\t{}: {} Goal(s)'.format(list(stats['home']['top3'].keys())[2],
                                          stats['home']['top3'][list(stats['home']['top3'].keys())[2]]))
    except:
        pass

    print('\t{}:'.format(away))
    print('\t\t{}: {} Goal(s)'.format(list(stats['away']['top3'].keys())[0],
                                      stats['away']['top3'][list(stats['away']['top3'].keys())[0]]))
    print('\t\t{}: {} Goal(s)'.format(list(stats['away']['top3'].keys())[1],
                                      stats['away']['top3'][list(stats['away']['top3'].keys())[1]]))
    try:
        print('\t\t{}: {} Goal(s)'.format(list(stats['away']['top3'].keys())[2],
                                          stats['away']['top3'][list(stats['away']['top3'].keys())[2]]))
    except:
        pass

    print('-------------------')

    print('Possible Results ({}-{}):'.format(home, away))
    idx = 0
    for result in stats['scores']:
        result_key = list(stats['scores'][idx].keys())[0]
        result_value = stats['scores'][idx][result_key]
        print('\t{}: {}'.format(result_key, result_value))
        idx += 1
