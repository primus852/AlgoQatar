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

    # Crawl all previous Cups
    cup.crawl_cup_df(2018)
    cup.crawl_cup_df(2014)
    cup.crawl_cup_df(2010)
    cup.crawl_cup_df(2006)
    cup.crawl_cup_df(2002)

    # Crawl current cup and put all in one folder
    cup.crawl_teams()
