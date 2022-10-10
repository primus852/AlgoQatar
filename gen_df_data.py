from src.Cup import Cup
from src.Util import Util
from src.Statistic import Statistic
from pprint import PrettyPrinter

if __name__ == '__main__':
    pp = PrettyPrinter(indent=4)

    driver = Util.setup_chrome()

    # Init the Classes early
    cup = Cup(driver)
    stats = Statistic()

    # TODO: Make this dynamic (argparse) and robust to errors
    wcs = [2018, 2014, 2010, 2006, 2002]

    # Crawl all previous Cups
    for wc in wcs:
        cup.crawl_cup_df(wc)

    # Crawl current cup and put all in one folder
    cup.crawl_teams()
