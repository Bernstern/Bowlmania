import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


import pandas as pd
import numpy as np
from fuzzywuzzy import process
# import matplotlib.pyplot as plt
# import tensorflow as tf

# Kaggle datasets used
# https://www.kaggle.com/datasets/mattop/college-football-bowl-games-1902-2022
# https://www.kaggle.com/datasets/jeffgallini/college-football-team-stats-2019?select=cfb17.csv
# https://www.kaggle.com/datasets/thedevastator/analyzing-college-football-2022-wins-losses-rank?select=games2022.csv

def load_stats() -> pd.DataFrame:
    stats_list = []
    # TODO: Include 2022
    for yr in range(13, 22):
        print(f"Loading data/cfb{yr}.csv")
        df = pd.read_csv(f'data/cfb{yr}.csv')

        # Make sure there are no unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Add year column
        df['year'] = yr

        stats_list.append(df)

    print("Concatenating stats")

    stats_df = pd.concat(stats_list, sort=False)
    # Drop any columns that are have any missing values
    stats_df = stats_df.dropna(axis=1, how='any')

    assert "Team" in stats_df.columns, "Team column not found"

    # Sanitize the stats data
    # Remove the division from the team name
    stats_df['Team'] = stats_df['Team'].str.replace(r'\([^\(\)]*\)$', '')

    # Strip out spaces and special characters
    stats_df['Team'] = stats_df['Team'].str.replace(r'[^a-zA-Z0-9\(\)]', '')

    # Remove the banned columns
    BANNED_COLUMNS = [
        "Time.of.Possession",
        "Average.Time.of.Possession.per.Game",
    ]
    stats_df = stats_df.drop(columns=BANNED_COLUMNS)

    # TODO: Find hex ugly fucker

    # Output it to a csv for funs sake
    stats_df.to_csv('stats.csv', index=False)

    # Multi-index
    stats_multi_df = stats_df.set_index(['year', 'Team'])
    stats_multi_df.to_csv('stats_m.csv')
    return stats_multi_df

def load_training_data():
    # Load up the all bowl games csv
    bowl_games = pd.read_csv("data/all_bowl_games.csv")

    # see how many gamse were played in the last 9 years
    bowl_games = bowl_games[bowl_games['year'] >= 2013]

    # Write these back to a csv
    bowl_games.to_csv('data/all_bowl_games.csv', index=False)

    # Create a new dataframe with the columns we want
    # training_data = pd.DataFrame(columns=['year', 'team1', 'team2', 'team1_win'] + ["1_" + col for col in team_data_cols] + ["2_" + col for col in team_data_cols])
    columns = ['year', 'team0', 'team1', 'winning_team']
    training_data = pd.DataFrame(columns=columns)

    for i, row in bowl_games.iterrows():
        year = row["year"] % 100
        if np.random.rand() > .5:
            new_row = [
                year, 
                row['winner_tie'],
                row['loser_tie'],
                0,
            ]   
        else:
            new_row = [
                year, 
                row['loser_tie'],
                row['winner_tie'],
                1,
            ]
        # Add the add the row to the training data
        training_data.loc[len(training_data)] = new_row # type: ignore
    training_data.to_csv('training_data.csv', index=False)
    return training_data
    
# Handle name fixing
def unfuck_names(name) -> str:
    custom_mapping = {
        "Texas Christian": "TCU",
        "Army": "Army West Point",
        "Middle Tennessee State": "Middle Tenn",
        "Florida International": "FIU",
        "Alabama-Birmingham": "UAB",
        "Central Florida": "UCF",
        "South Florida": "South Fla",
        "Miami": "Miami (FL)",
        "Connecticut": "UConn",
        "North Carolina State": "NCState",
        "Appalachian State": "App State",
        "Bringham Young": "BYU",
        "Brigham Young": "BYU",
        "Southern Methodist": "SMU",
        "Florida Atlantic": "Fla Atlantic",
        "Northern Illinois": "NIU",
        "Southern Michigan": "Southern Mich",
        "Central Michigan": "Central Mich",
        "Western Michigan": "Western Mich",
        "Eastern Michigan": "Eastern Mich",
        "Georgia Southern": "Ga Southern",
        "Bowling Green State": "Bowling Green",
        "Western Kentucky": "Western Ky",
        "Louisiana State": "Louisiana",
        "Colorado State": "Colorado",
        "Utah State": "Utah",
        "Texas-San Antonio": "UTSA",
        "Texas A&M": "Texas AM",
        "Southern Ole Miss": "Ole Miss",
        "Nevada-Las Vegas": "UNLV",
        "Texas-El Paso": "UTEP",
        "New Mexico": "New Mexico State",
    }

    # Check if the name is in the custom mapping
    name = custom_mapping.get(name, name)

    # Remove special characters
    name = name.replace(r'[^a-zA-Z0-9\(\)]', '')

    # Convert State to St
    name = name.replace('State', 'St')

    # Remove spaces
    name = name.replace(' ', '')

    return name

def teams_to_stats(stats, year, team0, team1):

    team0 = unfuck_names(team0)
    team1 = unfuck_names(team1)

    # Check that the teams are in the stats
    if team0 not in stats.loc[year].index:
        # Find the closest name to the team
        closest = process.extract(team0, stats.loc[year].index)[0]

        raise Exception(f'{team0} not in stats for year {year} - did you mean {closest}?')

    if team1 not in stats.loc[year].index:
        closest = process.extract(team1, stats.loc[year].index)[0]

        raise Exception(f'{team1} not in stats for year {year} - did you mean {closest}?')

    # df = pd.concat([stats.loc[year,team0], stats.loc[year,team1]], axis=1)
    # print(df.loc[:,(16,'Buffalo (MAC)')])
    df = stats.loc[(year,[team0, team1]), :]
    big_vector = list(df.iloc[0]) + list(df.iloc[1])
    return big_vector

if __name__ == "__main__":
    stats = load_stats()
    training_data = load_training_data()

    converted_training_data = []

    # Create a df of new training data using the team_to_stats function with the input from the training data df
    for i, row in training_data.iterrows():
        print(f"Processing row {i} of {len(training_data)}")
        training_data.append(teams_to_stats(stats, row['year'], row['team0'], row['team1']))

    print("Done processing training data!")

