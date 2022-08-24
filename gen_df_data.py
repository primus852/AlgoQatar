from src.Cup import Cup
from src.Util import Util
from pprint import PrettyPrinter

if __name__ == '__main__':
    pp = PrettyPrinter(indent=4)

    driver = Util.setup_chrome()

    cup = Cup(driver)

    # Crawl all previous Cups
    cup.crawl_cup_df(2018)
    cup.crawl_cup_df(2014)
    cup.crawl_cup_df(2010)
    cup.crawl_cup_df(2006)

    # Crawl current cup to see what is missing
    cup.crawl_missing_df()
