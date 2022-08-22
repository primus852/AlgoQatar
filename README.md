# Algorithm for the Qatar World Cup 2022

## Foreword

The final dataframe is a complete list of all teams participating in the World Cup 2022. It can be used for
a [Poisson Process](https://en.wikipedia.org/wiki/Poisson_point_process) for example to determine a probable outcome for
a given match.

Given a goal-scoring rate (avg. goals per 90 minutes), we can create
a [Gamma Distribution](https://en.wikipedia.org/wiki/Gamma_distribution), which can be used to show the probability for
certain amount of goals.

## Step 1 - Crawl Data

In order to generate all data, please run `gen_df_data.py`. This will get all data from specified Cups.

-

Example: `_gen_cup_df('wc18', 2018, 'https://fbref.com/en/comps/1/2018/schedule/2018-FIFA-World-Cup-Scores-and-Fixtures')`
will get all stats from all players who participated in the 2018 World Cup.

Repeating that method with various other Cups will generate summaries per Team per Cup in individual CSVs and their
folders.

**Please note**:
If a player participated in multiple cups, he will only be attributed once in the final dataframe, as the stats are
already averaged stats throughout his TOTAL career (all games played in the respecting national team).

## Step 2 - Add missing Teams (NYI)

Since not all teams have participated before, teams can be added manually by `gen_df_teams.py`. Update `team_links` with
the according link to start the crawling for all players of the team. This link needs to be from
the [WC Qualifier 2022](https://fbref.com/en/comps/1/qual/FIFA-World-Cup-Qualifying-Rounds).

Example:

```python
team_links = [
    {
        'link': 'https://fbref.com/en/squads/896550da/2022/Cameroon-Men-Stats',
        'country': 'Cameroon'
    }
]
```

## Step 3 - Add missing players (NYI)

Since there are some players who never participated in any previous tournament, some players need to be added manually.
For that, please use `gen_df_players.py`. Update `player_links` with all Links from fbref.com of missing players and
their country.

Example:

```python
player_links = [
    {
        'link': 'https://fbref.com/en/players/44c3d1d2/Aleksandr-Samedov',
        'country': 'Russia'
    }
]
```
