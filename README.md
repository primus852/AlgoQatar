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

Example: `_gen_cup_df(2018)`
will get all stats from all players who participated in the 2018 World Cup.

Repeating that method with various other Cups will generate summaries per Team per Cup in individual CSVs and their
folders.

**Please note**:
If a player participated in multiple cups, he will only be attributed once in the final dataframe, as the stats are
already averaged stats throughout his TOTAL career (all games played in the respecting national team).

After every team (and the games) has been crawled, the script will run through all the participants of the CURRENT cup
and add them as well.
