import cfbd
import pandas as pd

configuration = cfbd.Configuration()
configuration.api_key["Authorization"] = "REPLACE"
configuration.api_key_prefix["Authorization"] = "Bearer"

YEARS = range(2013, 2023)

games_api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
teams_api_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))


def get_games(year):
    games_dicts = []

    for season in ["regular", "postseason"]:
        for division in ["fbs", "fcs"]:
            games = games_api_instance.get_games(
                year=year, season_type=season, division=division
            )

            for game in games:
                if game.home_points is None or game.away_points is None:
                    continue

                game_data = {
                    "year": game.season,
                    "0_team": game.home_team,
                    "1_team": game.away_team,
                    "winner_id": 0 if game.home_points > game.away_points else 1,
                }
                games_dicts.append(game_data)

    return pd.DataFrame(games_dicts)


games_dfs = []
for year in range(2013, 2024):
    print(f"Getting games for {year}")
    games_dfs.append(get_games(year))

games_df = pd.concat(games_dfs)

games_df.to_csv("data/games.csv", index=False)
