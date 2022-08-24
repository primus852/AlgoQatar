from src.Util import Util
from scipy.stats import poisson
from scipy.stats import gamma
from empiricaldist import Pmf
import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations


class Poisson:

    @staticmethod
    def decorate_goals(title=''):
        Util.decorate(xlabel='Number of goals', ylabel='PMF', title=title)

    @staticmethod
    def decorate_rate(title=''):
        Util.decorate(xlabel='Goal scoring rate (lam)', ylabel='PMF', title=title)

    @staticmethod
    def update_poisson(pmf, data):
        """Update Pmf with a Poisson likelihood."""
        k = data
        lams = pmf.qs
        likelihood = poisson(lams).pmf(k)
        pmf *= likelihood
        pmf.normalize()

        return pmf

    def __calc(self, avg_goals: float, team: str, plot: bool):
        pmf = Util.make_poisson_pmf(avg_goals, np.arange(10))

        if plot:
            pmf.bar(label=r'Poisson distribution with $\lambda={}$'.format(avg_goals))
            self.decorate_goals('Dist of goals scored ({})'.format(team))
            plt.show()

        return pmf

    @staticmethod
    def __raw(pmf) -> dict:
        return {
            '0': round(pmf[0] * 100, 1),
            '1': round(pmf[1] * 100, 1),
            '2': round(pmf[2] * 100, 1),
            '3': round(pmf[3] * 100, 1),
            '4': round(pmf[4] * 100, 1),
            '5': round(pmf[5] * 100, 1),
            '6': round(pmf[6] * 100, 1),
            '7': round(pmf[7] * 100, 1),
            '8': round(pmf[8] * 100, 1),
            '9': round(pmf[9] * 100, 1),
        }

    @staticmethod
    def __top3(raw_pmf: dict):
        x = sorted(raw_pmf.items(), key=(lambda i: i[1]))

        return {
            '{}%'.format(x[-1][1]): x[-1][0],
            '{}%'.format(x[-2][1]): x[-2][0],
            '{}%'.format(x[-3][1]): x[-3][0],
        }

    def calculate(self, avg_goals_home: float, avg_goals_away: float, team_home: str, team_away: str,
                  plot: bool = False):
        pmf_home = self.__calc(avg_goals_home, team_home, plot)
        pmf_away = self.__calc(avg_goals_away, team_away, plot)

        raw_home = self.__raw(pmf_home)
        raw_away = self.__raw(pmf_away)

        top3_home = self.__top3(raw_home)
        top3_away = self.__top3(raw_away)

        win = Pmf.prob_gt(pmf_home, pmf_away)
        lose = Pmf.prob_lt(pmf_home, pmf_away)
        tie = Pmf.prob_eq(pmf_home, pmf_away)

        possible_scores = []
        for key_home in top3_home:
            for key_away in top3_away:
                pct_raw_home = raw_home['{}'.format(top3_home[key_home])] / 100
                pct_raw_away = raw_away['{}'.format(top3_away[key_away])] / 100
                result_pct = round(pct_raw_home * pct_raw_away * 100, 2)
                possible_scores.append({
                    '{}-{}'.format(top3_home[key_home], top3_away[key_away]): '{}%'.format(result_pct)
                })

        return {
            'home': {
                'team': team_home,
                'goals_per_90': avg_goals_home,
                'raw': raw_home,
                'top3': top3_home
            },
            'away': {
                'team': team_away,
                'goals_per_90': avg_goals_away,
                'raw': raw_away,
                'top3': top3_away
            },
            'outcome': {
                'win_home': win,
                'lose_home': lose,
                'tie': tie
            },
            'scores': possible_scores
        }
