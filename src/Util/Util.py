from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from empiricaldist import Pmf
from statsmodels.nonparametric.smoothers_lowess import lowess
from seaborn import JointGrid

from scipy.stats import gaussian_kde
from scipy.stats import binom
from scipy.stats import gamma
from scipy.stats import poisson


class Util:
    @staticmethod
    def values(series):
        """Make a series of values and the number of times they appear.

        Returns a DataFrame because they get rendered better in Jupyter.

        series: Pandas Series

        returns: Pandas DataFrame
        """
        series = series.value_counts(dropna=False).sort_index()
        series.index.name = 'values'
        series.name = 'counts'
        return pd.DataFrame(series)

    @staticmethod
    def write_table(table, label, **options):
        """Write a table in LaTex format.

        table: DataFrame
        label: string
        options: passed to DataFrame.to_latex
        """
        filename = f'tables/{label}.tex'
        fp = open(filename, 'w')
        s = table.to_latex(**options)
        fp.write(s)
        fp.close()

    @staticmethod
    def write_pmf(pmf, label):
        """Write a Pmf object as a table.

        pmf: Pmf
        label: string
        """
        df = pd.DataFrame()
        df['qs'] = pmf.index
        df['ps'] = pmf.values
        Util.write_table(df, label, index=False)

    @staticmethod
    def underride(d, **options):
        """Add key-value pairs to d only if key is not in d.

        d: dictionary
        options: keyword args to add to d
        """
        for key, val in options.items():
            d.setdefault(key, val)

        return d

    @staticmethod
    def decorate(**options):
        """Decorate the current axes.

        Call decorate with keyword arguments like
        decorate(title='Title',
                 xlabel='x',
                 ylabel='y')

        The keyword arguments can be any of the axis properties
        https://matplotlib.org/api/axes_api.html
        """
        ax = plt.gca()
        ax.set(**options)

        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend(handles, labels)

        plt.tight_layout()

    @staticmethod
    def savefig(root, **options):
        """Save the current figure.

        root: string filename root
        options: passed to plt.savefig
        """
        format_opt = options.pop('format', None)
        if format_opt:
            formats = [format_opt]
        else:
            formats = ['pdf', 'png']

        for format_opt in formats:
            fname = f'figs/{root}.{format_opt}'
            plt.savefig(fname, **options)

    @staticmethod
    def make_die(sides):
        """Pmf that represents a die with the given number of sides.

        sides: int

        returns: Pmf
        """
        outcomes = np.arange(1, sides + 1)
        die = Pmf(1 / sides, outcomes)
        return die

    @staticmethod
    def add_dist_seq(seq):
        """Distribution of sum of quantities from PMFs.

        seq: sequence of Pmf objects

        returns: Pmf
        """
        total = seq[0]
        for other in seq[1:]:
            total = total.add_dist(other)
        return total

    @staticmethod
    def make_mixture(pmf, pmf_seq):
        """Make a mixture of distributions.

        pmf: mapping from each hypothesis to its probability
             (or it can be a sequence of probabilities)
        pmf_seq: sequence of Pmfs, each representing
                 a conditional distribution for one hypothesis

        returns: Pmf representing the mixture
        """
        df = pd.DataFrame(pmf_seq).fillna(0).transpose()
        df *= np.array(pmf)
        total = df.sum(axis=1)
        return Pmf(total)

    @staticmethod
    def summarize(posterior, prob=0.9):
        """Print the mean and CI of a distribution.

        posterior: Pmf
        digits: number of digits to round to
        prob: probability in the CI
        """
        mean = np.round(posterior.mean(), 3)
        ci = posterior.credible_interval(prob)
        print(mean, ci)

    @staticmethod
    def outer_product(s1, s2):
        """Compute the outer product of two Series.

        First Series goes down the rows;
        second goes across the columns.

        s1: Series
        s2: Series

        return: DataFrame
        """
        a = np.multiply.outer(s1.to_numpy(), s2.to_numpy())
        return pd.DataFrame(a, index=s1.index, columns=s2.index)

    @staticmethod
    def make_uniform(qs, name=None, **options):
        """Make a Pmf that represents a uniform distribution.

        qs: quantities
        name: string name for the quantities
        options: passed to Pmf

        returns: Pmf
        """
        pmf = Pmf(1.0, qs, **options)
        pmf.normalize()
        if name:
            pmf.index.name = name
        return pmf

    @staticmethod
    def make_joint(s1, s2):
        """Compute the outer product of two Series.

        First Series goes across the columns;
        second goes down the rows.

        s1: Series
        s2: Series

        return: DataFrame
        """
        x, y = np.meshgrid(s1, s2)
        return pd.DataFrame(x * y, columns=s1.index, index=s2.index)

    @staticmethod
    def make_mesh(joint):
        """Make a mesh grid from the quantities in a joint distribution.

        joint: DataFrame representing a joint distribution

        returns: a mesh grid (X, Y) where X contains the column names and
                                          Y contains the row labels
        """
        x = joint.columns
        y = joint.index
        return np.meshgrid(x, y)

    @staticmethod
    def normalize(joint):
        """Normalize a joint distribution.

        joint: DataFrame
        """
        prob_data = joint.to_numpy().sum()
        joint /= prob_data
        return prob_data

    @staticmethod
    def marginal(joint, axis):
        """Compute a marginal distribution.

        axis=0 returns the marginal distribution of the first variable
        axis=1 returns the marginal distribution of the second variable

        joint: DataFrame representing a joint distribution
        axis: int axis to sum along

        returns: Pmf
        """
        return Pmf(joint.sum(axis=axis))

    @staticmethod
    def pmf_marginal(joint_pmf, level):
        """Compute a marginal distribution.

        joint_pmf: Pmf representing a joint distribution
        level: int, level to sum along

        returns: Pmf
        """
        return Pmf(joint_pmf.sum(level=level))

    @staticmethod
    def plot_contour(joint, **options):
        """Plot a joint distribution.

        joint: DataFrame representing a joint PMF
        """
        low = joint.to_numpy().min()
        high = joint.to_numpy().max()
        levels = np.linspace(low, high, 6)
        levels = levels[1:]

        Util.underride(options, levels=levels, linewidths=1)
        cs = plt.contour(joint.columns, joint.index, joint, **options)
        Util.decorate(xlabel=joint.columns.name,
                      ylabel=joint.index.name)
        return cs

    @staticmethod
    def make_binomial(n, p):
        """Make a binomial distribution.

        n: number of trials
        p: probability of success

        returns: Pmf representing the distribution of k
        """
        ks = np.arange(n + 1)
        ps = binom.pmf(ks, n, p)
        return Pmf(ps, ks)

    @staticmethod
    def make_gamma_dist(alpha, beta):
        """Makes a gamma object.

        alpha: shape parameter
        beta: scale parameter

        returns: gamma object
        """
        dist = gamma(alpha, scale=1 / beta)
        dist.alpha = alpha
        dist.beta = beta
        return dist

    @staticmethod
    def make_poisson_pmf(lam, qs):
        """Make a PMF of a Poisson distribution.

        lam: event rate
        qs: sequence of values for `k`

        returns: Pmf
        """
        ps = poisson(lam).pmf(qs)
        pmf = Pmf(ps, qs)
        pmf.normalize()
        return pmf

    @staticmethod
    def pmf_from_dist(dist, qs):
        """Make a discrete approximation.

        dist: SciPy distribution object
        qs: quantities

        returns: Pmf
        """
        ps = dist.pdf(qs)
        pmf = Pmf(ps, qs)
        pmf.normalize()
        return pmf

    @staticmethod
    def kde_from_sample(sample, qs, **options):
        """Make a kernel density estimate from a sample

        sample: sequence of values
        qs: quantities where we should evaluate the KDE

        returns: normalized Pmf
        """
        kde = gaussian_kde(sample)
        ps = kde(qs)
        pmf = Pmf(ps, qs, **options)
        pmf.normalize()
        return pmf

    @staticmethod
    def kde_from_pmf(pmf, n=101, **options):
        """Make a kernel density estimate from a Pmf.

        pmf: Pmf object
        n: number of points

        returns: Pmf object
        """
        kde = gaussian_kde(pmf.qs, weights=pmf.ps)
        qs = np.linspace(pmf.qs.min(), pmf.qs.max(), n)
        ps = kde.evaluate(qs)
        pmf = Pmf(ps, qs, **options)
        pmf.normalize()
        return pmf

    @staticmethod
    def make_lowess(series):
        """Use LOWESS to compute a smooth line.

        series: pd.Series

        returns: pd.Series
        """
        endog = series.values
        exog = series.index.values

        smooth = lowess(endog, exog)
        index, data = np.transpose(smooth)

        return pd.Series(data, index=index)

    @staticmethod
    def plot_series_lowess(series, color):
        """Plots a series of data points and a smooth line.

        series: pd.Series
        color: string or tuple
        """
        series.plot(lw=0, marker='o', color=color, alpha=0.5)
        smooth = Util.make_lowess(series)
        smooth.plot(label='_', color=color)

    @staticmethod
    def joint_plot(joint, **options):
        """Show joint and marginal distributions.

        joint: DataFrame that represents a joint distribution
        options: passed to JointGrid
        """
        # get the names of the parameters
        x = joint.columns.name
        x = 'x' if x is None else x

        y = joint.index.name
        y = 'y' if y is None else y

        # make a JointGrid with minimal data
        data = pd.DataFrame({x: [0], y: [0]})
        g = JointGrid(x, y, data, **options)

        # replace the contour plot
        g.ax_joint.contour(joint.columns,
                           joint.index,
                           joint,
                           cmap='viridis')

        # replace the marginals
        marginal_x = Util.marginal(joint, 0)
        g.ax_marg_x.plot(marginal_x.qs, marginal_x.ps)

        marginal_y = Util.marginal(joint, 1)
        g.ax_marg_y.plot(marginal_y.ps, marginal_y.qs)

    Gray20 = (0.162, 0.162, 0.162, 0.7)
    Gray30 = (0.262, 0.262, 0.262, 0.7)
    Gray40 = (0.355, 0.355, 0.355, 0.7)
    Gray50 = (0.44, 0.44, 0.44, 0.7)
    Gray60 = (0.539, 0.539, 0.539, 0.7)
    Gray70 = (0.643, 0.643, 0.643, 0.7)
    Gray80 = (0.757, 0.757, 0.757, 0.7)
    Pu20 = (0.247, 0.0, 0.49, 0.7)
    Pu30 = (0.327, 0.149, 0.559, 0.7)
    Pu40 = (0.395, 0.278, 0.62, 0.7)
    Pu50 = (0.46, 0.406, 0.685, 0.7)
    Pu60 = (0.529, 0.517, 0.742, 0.7)
    Pu70 = (0.636, 0.623, 0.795, 0.7)
    Pu80 = (0.743, 0.747, 0.866, 0.7)
    Bl20 = (0.031, 0.188, 0.42, 0.7)
    Bl30 = (0.031, 0.265, 0.534, 0.7)
    Bl40 = (0.069, 0.365, 0.649, 0.7)
    Bl50 = (0.159, 0.473, 0.725, 0.7)
    Bl60 = (0.271, 0.581, 0.781, 0.7)
    Bl70 = (0.417, 0.681, 0.838, 0.7)
    Bl80 = (0.617, 0.791, 0.882, 0.7)
    Gr20 = (0.0, 0.267, 0.106, 0.7)
    Gr30 = (0.0, 0.312, 0.125, 0.7)
    Gr40 = (0.001, 0.428, 0.173, 0.7)
    Gr50 = (0.112, 0.524, 0.253, 0.7)
    Gr60 = (0.219, 0.633, 0.336, 0.7)
    Gr70 = (0.376, 0.73, 0.424, 0.7)
    Gr80 = (0.574, 0.824, 0.561, 0.7)
    Or20 = (0.498, 0.153, 0.016, 0.7)
    Or30 = (0.498, 0.153, 0.016, 0.7)
    Or40 = (0.599, 0.192, 0.013, 0.7)
    Or50 = (0.746, 0.245, 0.008, 0.7)
    Or60 = (0.887, 0.332, 0.031, 0.7)
    Or70 = (0.966, 0.475, 0.147, 0.7)
    Or80 = (0.992, 0.661, 0.389, 0.7)
    Re20 = (0.404, 0.0, 0.051, 0.7)
    Re30 = (0.495, 0.022, 0.063, 0.7)
    Re40 = (0.662, 0.062, 0.085, 0.7)
    Re50 = (0.806, 0.104, 0.118, 0.7)
    Re60 = (0.939, 0.239, 0.178, 0.7)
    Re70 = (0.985, 0.448, 0.322, 0.7)
    Re80 = (0.988, 0.646, 0.532, 0.7)

    from cycler import cycler

    color_list = [Bl30, Or70, Gr50, Re60, Pu20, Gray70, Re80, Gray50,
                  Gr70, Bl50, Re40, Pu70, Or50, Gr30, Bl70, Pu50, Gray30]
    color_cycle = cycler(color=color_list)

    @staticmethod
    def set_pyplot_params():
        plt.rcParams['axes.prop_cycle'] = Util.color_cycle
        plt.rcParams['lines.linewidth'] = 3

    @staticmethod
    def setup_chrome() -> uc.Chrome:
        """
        Init the Chrome Driver to pass to classes
        Also click the cookie banner to make ads show
        """
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = uc.Chrome(executable_path="chrome/chromedriver.exe", chrome_options=options)

        driver.get('https://fbref.com/en/')
        time.sleep(2)
        agree_button = driver.find_element(By.XPATH, "//button[contains(text(),'AGREE')]")
        agree_button.click()

        return driver

    @staticmethod
    def load_players_by_team(team) -> pd.DataFrame:
        return pd.read_csv('data/wcCurrent/{}.csv'.format(team))

    @staticmethod
    def load_teams_from_current(keep_ending=True) -> list:

        teams = []
        for file in os.listdir('data/wcCurrent'):
            if keep_ending:
                teams.append(file)
            else:
                teams.append(file.replace('.csv', ''))

        return teams

    @staticmethod
    def merge_games_to_df():

        df = pd.DataFrame(columns=['home', 'away', 'score_home', 'score_away'])

        folders = [dI for dI in os.listdir('data') if os.path.isdir(os.path.join('data', dI))]
        for folder in folders:
            if folder == 'wcCurrent':
                continue
            for file in os.listdir('data/{}/games'.format(folder)):
                df_load = pd.read_csv('data/{}/games/{}'
                                      .format(folder, file), usecols=['home', 'away', 'score_home', 'score_away'])
                df = pd.concat([df, df_load])

        return df
