import time
import os
from io import StringIO
from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import progressbar


# Make sure lxml, beautifulsoup4 and html5lib are installed
# pip install lxml html5lib beautifulsoup4

DROPPED_COLS = ["Rank", "KO TB"]

SPECIFIC_DROP_COLS = {"Total Offense": ["TDs"]}

STAT_GROUPS = {
    "Total Offense": [
        "Team",
        "Games",
        "Win-Loss",
        "Off Plays",
        "Off Yards",
        "Off Yards/Play",
        "Off TDs",
        "Off Yards per Game",
    ],
    "Total Defense": [
        "Team",
        "Games",
        "Win-Loss",
        "Def Plays",
        "Yards Allowed",
        "Yards/Play Allowed",
        "Off TDs Allowed",
        "Total TDs Allowed",
        "Yards Per Game Allowed",
    ],
    "Turnover Margin": [
        "Team",
        "Games",
        "Win-Loss",
        "Fumbles Recovered",
        "Opponents Intercepted",
        "Turnovers Gain",
        "Fumbles Lost",
        "Interceptions Thrown",
        "Turnovers Lost",
        "Turnover Margin",
        "Avg Turnover Margin per Game",
    ],
    "Time of Possession": [
        "Team",
        "Games",
        "Win-Loss",
        "Time of Possession",
        "Average Time of Possession per Game",
    ],
    "Team Tackles for Loss": [
        "Team",
        "Games",
        "Win-Loss",
        "Solo Tackle For Loss",
        "Assist Tackle For Loss",
        "Tackle for Loss Yards",
        "Total Tackle For Loss",
        "Tackle For Loss Per Game",
    ],
    "Sacks Allowed": [
        "Team",
        "Games",
        "Win-Loss",
        "Sacks",
        "Sack Yards",
        "Average Sacks per Game",
    ],
    "Scoring Offense": [
        "Team",
        "Games",
        "Win-Loss",
        "Touchdowns",
        "PAT",
        "2 Point Conversions",
        "Defensive Points",
        "Feild Goals",
        "Safety",
        "Total Points",
        "Points Per Game",
    ],
    "Scoring Defense": [
        "Team",
        "Games",
        "Win-Loss",
        "Touchdowns Allowed",
        "Opponent Extra Points",
        "2 Point Conversions Allowed",
        "Opp Deflected Extra Points",
        "Opp Feild Goals Made",
        "Opp Safety",
        "Points Allowed",
        "Avg Points per Game Allowed",
    ],
    "Rushing Offense": [
        "Team",
        "Games",
        "Win-Loss",
        "Rush Attempts",
        "Rush Yds",
        "Yards/Rush",
        "Rushing TD",
        "Rushing Yards per Game",
    ],
    "Rushing Defense": [
        "Team",
        "Games",
        "Win-Loss",
        "Opp Rush Attempts",
        "Opp Rush Yards Alloweed",
        "Yds/Rush Allowed",
        "Opp Rush Touchdowns Allowed",
        "Rush Yards Per Game Allowed",
    ],
    "Red Zone Offense": [
        "Team",
        "Games",
        "Win-Loss",
        "Redzone Attempts",
        "Redzone Rush TD",
        "Redzone Pass TD",
        "Redzone Field Goals Made",
        "Redzone Scores",
        "Redzone Points",
    ],
    "Red Zone Defense": [
        "Team",
        "Games",
        "Win-Loss",
        "Opp Redzone Attempts",
        "Opp Redzone Rush TD Allowed",
        "Opp Redzone Pass Touchdowns Allowed",
        "Opp Redzone Field Goals Made",
        "Opp Redzone Scores",
        "Redzone Points Allowed",
    ],
    "Punt Return": [
        "Team",
        "Games",
        "Win-Loss",
        "Punt Returns",
        "Net Punt Return Yards",
        "Punt Return Touchdowns",
        "Avg Yards Per Punt Return",
    ],
    "Punt Return Defense": [
        "Team",
        "Games",
        "Win-Loss",
        "Opp Punt Returns",
        "Opp Net Punt Return Yards",
        "Opp Punt Return Touchdowns Allowed",
        "Avg Yards Allowed per Punt Return",
    ],
    "Passing Offense": [
        "Team",
        "Games",
        "Win-Loss",
        "Pass Attempts",
        "Pass Completions",
        "Passing Interceptions Thrown",
        "Pass Yards",
        "Pass Yards/Attempt",
        "Yards/Completion",
        "Pass Touchdowns",
        "Pass Yards Per Game",
    ],
    "Passing Yards Allowed": [
        "Team",
        "Games",
        "Win-Loss",
        "Opp Completions Allowed",
        "Opp Pass Attempts",
        "Opp Pass Yds Allowed",
        "Opp Pass TDs Allowed",
        "Yards/Attempt Allowed",
        "Yards/Completion Allowed",
        "Pass Yards Per Game Allowed",
    ],
    "Kickoff Return": [
        "Team",
        "Games",
        "Win-Loss",
        "Kickoffs Returned",
        "Kickoff Return Yards",
        "Kickoff Return Touchdowns",
        "Avg Yard per Kickoff Return",
    ],
    "Kickoff Return Defense": [
        "Team",
        "Games",
        "Win-Loss",
        "Opp Kickoff Returns",
        "Opponent Kickoff Return Yards",
        "Opp Kickoff Return Touchdowns Allowed",
        "Avg Yards per Kickoff Return Allowed",
    ],
    "First Down Offense": [
        "Team",
        "Games",
        "Win-Loss",
        "First Down Runs",
        "First Down Passes",
        "First Down Penalties",
        "First Downs",
    ],
    "First Down Defense": [
        "Team",
        "Games",
        "Win-Loss",
        "Opp First Down Runs",
        "Opp First Down Passes",
        "Opp First Down Penalties",
        "Opp First Downs",
    ],
    "Fewest Penalty Yards Per Game": [
        "Team",
        "Games",
        "Win-Loss",
        "Penalties",
        "Penalty Yards",
        "Penalty Yards Per Game",
    ],
    "3rd Down Conversion Pct": [
        "Team",
        "Games",
        "Win-Loss",
        "3rd Attempts",
        "3rd Conversions",
        "3rd Percent",
    ],
    "3rd Down Conversion Pct Defense": [
        "Team",
        "Games",
        "Win-Loss",
        "Opp 3rd Conversion",
        "Opp 3rd Attempt",
        "Opponent 3rd Percent",
    ],
    "4th Down Conversion Pct": [
        "Team",
        "Games",
        "Win-Loss",
        "4th Attempts",
        "4th Conversions",
        "4th Percent",
    ],
    "4th Down Conversion Pct Defense": [
        "Team",
        "Games",
        "Win-Loss",
        "Opp 4th Conversion",
        "Opp 4th Attempt",
        "Opponent 4th Percent",
    ],
}

JOIN_COLS = ["Team", "Games", "Win-Loss"]
DIVISIONS = [
    "11.0",
    "12.0",
]


def scrape_stat_category(year):
    # needs to be local for multiprocessing
    driver = webdriver.Chrome()
    driver.implicitly_wait(20)
    # driver.minimize_window()

    for division in DIVISIONS:
        print(f"Scraping Division {division}...")
        stats_url = f"https://stats.ncaa.org/rankings?academic_year={year}&division={division}&sport_code=MFB"

        driver.get(stats_url)
        for stat_group in progressbar.progressbar(STAT_GROUPS):
            filename = f"scraping/{year}/{division}/{stat_group}.csv"

            # Check if we already scraped this stat group
            if os.path.exists(filename):
                continue

            # Find the team tab
            team_tab = driver.find_element(By.ID, "stat_type_T_N")
            team_tab.click()

            # print(f"Scraping {stat_group}...")
            stat = driver.find_element(By.ID, "Stats")
            stat.click()

            # Select the stat group
            stat.send_keys(stat_group)
            stat.send_keys(Keys.RETURN)
            time.sleep(1)

            # Now we can see the full table, just need to see all 150 rows
            try:
                len = driver.find_element(By.NAME, "rankings_table_length")
                len.click()
                len.send_keys(Keys.DOWN)
                len.send_keys(Keys.RETURN)
                time.sleep(0.5)
            except:
                pass

            # Now we can rip the entire table (there's 2, we just want the latter)
            dfs = pd.read_html(StringIO(driver.page_source))[1]

            # Drop any rows that have "Reclassifying" in the Team column
            try:
                dfs = dfs[~dfs["Team"].str.contains("Reclassifying")]
            except KeyError:
                pass

            # Drop any columns that are in the dropped columns list
            dfs = dfs.drop(columns=DROPPED_COLS, errors="ignore")

            # Drop any columns that are in the specific dropped columns list
            if stat_group in SPECIFIC_DROP_COLS:
                dfs = dfs.drop(columns=SPECIFIC_DROP_COLS[stat_group], errors="ignore")

            # Update the column names
            try:
                dfs.columns = STAT_GROUPS[stat_group]
            except ValueError as e:
                print(f"Error with {stat_group} in {year} {e}")
                print(dfs.columns)
                print(STAT_GROUPS[stat_group])
                raise ValueError

            # Make the directory if it doesn't exist
            if not os.path.exists("scraping"):
                os.makedirs("scraping")

            if not os.path.exists(f"scraping/{year}"):
                os.makedirs(f"scraping/{year}")

            if not os.path.exists(f"scraping/{year}/{division}"):
                os.makedirs(f"scraping/{year}/{division}")

            # Write to CSV
            dfs.to_csv(f"scraping/{year}/{division}/{stat_group}.csv", index=False)

            time.sleep(1)


def scrape_year(YEAR):
    start_time = time.time()
    scrape_stat_category(str(YEAR))
    print(f"Scraping took {time.time() - start_time} seconds")

    # # Once we are done scraping we can merge all the csvs into one giant data frame and save it
    dfs = defaultdict(dict)
    for division in DIVISIONS:
        for stat_group in STAT_GROUPS:
            df = pd.read_csv(f"scraping/{YEAR}/{division}/{stat_group}.csv")
            dfs[division][stat_group] = df

    # First merge the stat groups across divisions
    merged_dfs = {}
    for stat_group in STAT_GROUPS:
        merged_dfs[stat_group] = pd.concat(
            [dfs[division][stat_group] for division in DIVISIONS]
        )

    # Now merge the stat groups together into one giant dataframe
    final_df = merged_dfs["Total Offense"]
    for stat_group in STAT_GROUPS:
        if stat_group == "Total Offense":
            continue
        final_df = final_df.merge(merged_dfs[stat_group], on=JOIN_COLS, how="outer")

    YEAR = f"{YEAR-1}-{YEAR}"
    final_df.to_csv(f"data/{YEAR}.csv", index=False)


for YEAR in range(2014, 2025):
    print(f"Scraping {YEAR}...")
    scrape_year(YEAR)
