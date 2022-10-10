from src.Cup import Cup
from src.Util import Util
from pprint import PrettyPrinter

if __name__ == '__main__':
    pp = PrettyPrinter(indent=4)

    driver = Util.setup_chrome()

    # Init the Classes early
    cup = Cup(driver)

    # Fix a certain Team of current Cup
    cup.crawl_team(team_link='https://fbref.com/en/squads/6a08f71e/IR-Iran-Men-Stats', team_name='IR Iran')
