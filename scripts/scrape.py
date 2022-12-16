# Okay the cursed r script doesn't work so I'm going to try to do it in python

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from multiprocessing import Pool
import pandas as pd

# Make sure lxml, beautifulsoup4 and html5lib are installed
# pip install lxml html5lib beautifulsoup4

stats_url = "https://stats.ncaa.org/rankings?academic_year=2023&division=11.0&sport_code=MFB/"


STAT_GROUPS = {
    "Total Offense":  ["Off Rank", "Team", "Games", "Win-Loss", "Off Plays", "Off Yards", "Off Yards/Play", "Off TDs", "Off Yards per Game"],
    "Total Defense":  ["Def Rank", "Team", "Games", "Win-Loss", "Def Plays", "Yards Allowed", "Yards/Play Allowed", "Off TDs Allowed", "Total TDs Allowed", "Yards Per Game Allowed" ],
    "Turnover Margin":  ["Turnover Rank", "Team", "Games", "Win-Loss", "Fumbles Recovered", "Opponents Intercepted", "Turnovers Gain", "Fumbles Lost", "Interceptions Thrown", "Turnovers Lost", "Turnover Margin", "Avg Turnover Margin per Game"],
    "Time of Possession":  ["Time of Possession Rank", "Team", "Games", "Win-Loss", "Time of Possession", "Average Time of Possession per Game"],
    "Team Tackles for Loss":  ["Tackle for Loss Rank", "Team", "Games", "Win-Loss", "Solo Tackle For Loss", "Assist Tackle For Loss", "Tackle for Loss Yards", "Total Tackle For Loss", "Tackle For Loss Per Game"],
    "Sacks Allowed":  ["Sack Rank", "Team", "Games", "Win-Loss",  "Sacks", "Sack Yards", "Average Sacks per Game" ],
    "Scoring Offense":  ["Scoring Off Rank", "Team", "Games",    "Win-Loss", "Touchdowns", "PAT", "2 Point Conversions", "Defensive Points", "Feild Goals", "Safety", "Total Points", "Points Per Game" ],
    "Scoring Defense":  ["Scoring Def Rank", "Team", "Games",   "Win-Loss", "Touchdowns Allowed", "Opponent Extra Points",  "2 Point Conversions Allowed", "Opp Deflected Extra Points", "Opp Feild Goals Made", "Opp Safety", "Points Allowed", "Avg Points per Game Allowed" ],
    "Rushing Offense":  ["Rushing Off Rank", "Team", "Games", "Win-Loss", "Rush Attempts", "Rush Yds", "Yards/Rush", "Rushing TD",  "Rushing Yards per Game"  ],
    "Rushing Defense":  ["Rushing Def Rank", "Team", "Games", "Win-Loss", "Opp Rush Attempts", "Opp Rush Yards Alloweed", "Yds/Rush Allowed",     "Opp Rush Touchdowns Allowed", "Rush Yards Per Game Allowed"],
    "Red Zone Offense":  ["Redzone Off Rank", "Team",  "Games"   ,"Win-Loss", "Redzone Attempts","Redzone Rush TD", "Redzone Pass TD", "Redzone Field Goals Made", "Redzone Scores", "Redzone Points"],
    "Red Zone Defense":  ["Redzone Def Rank", "Team", "Games", "Win-Loss", "Opp Redzone Attempts", "Opp Redzone Rush TD Allowed","Opp Redzone Pass Touchdowns Allowed", "Opp Redzone Field Goals Made", "Opp Redzone Scores", "Redzone Points Allowed"],
    "Punt Return":  ["Punt Return Rank", "Team", "Games", "Win-Loss", "Punt Returns", "Net Punt Return Yards", "Punt Return Touchdowns", "Avg Yards Per Punt Return" ],
    "Punt Return Defense":  ["Punt Return Def Rank", "Team", "Games",  "Win-Loss", "Opp Punt Returns", "Opp Net Punt Return Yards", "Opp Punt Return Touchdowns Allowed", "Avg Yards Allowed per Punt Return"],
    "Passing Offense":  ["Passing Off Rank", "Team", "Games", "Win-Loss", "Pass Attempts", "Pass Completions", "Interceptions Thrown",  "Pass Yards", "Pass Yards/Attempt",  "Yards/Completion", "Pass Touchdowns", "Pass Yards Per Game"],
    "Passing Yards Allowed":  ["Pass Def Rank", "Team", "Games",  "Win-Loss", "Opp Completions Allowed", "Opp Pass Attempts", "Opp Pass Yds Allowed", "Opp Pass TDs Allowed", "Yards/Attempt Allowed", "Yards/Completion Allowed", "Pass Yards Per Game Allowed"],
    "Kickoff Return":  ["Kickoff Return Rank", "Team", "Games", "Win-Loss","Kickoffs Returned", "Kickoff Return Yards", "Kickoff Return Touchdowns", "Avg Yard per Kickoff Return", "REMOVE" ], # TODO: There is a bug in the NCAA stats website that causes this to not work
    "Kickoff Return Defense":  ["Kickoff Return Def Rank", "Team", "Games", "Win-Loss", "Opp Kickoff Returns","Kickoff Touchbacks", "Opponent Kickoff Return Yards", "Opp Kickoff Return Touchdowns Allowed", "Avg Yards per Kickoff Return Allowed"],
    "First Down Offense":  ["First Down Rank", "Team", "Games","Win-Loss", "First Down Runs", "First Down Passes", "First Down Penalties", "First Downs" ],
    "First Down Defense":  ["First Down Def Rank", "Team", "Games","Win-Loss", "Opp First Down Runs", "Opp First Down Passes", "Opp First Down Penalties", "Opp First Downs" ],
    "Fewest Penalty Yards Per Game":  ["Penalty Rank", "Team", "Games", "Win-Loss", "Penalties", "Penalty Yards", "Penalty Yards Per Game"],
    "3rd Down Conversion Pct": ["3rd Down Rank", "Team", "Games", "Win-Loss","3rd Attempts", "3rd Conversions", "3rd Percent"],
    "3rd Down Conversion Pct Defense": ["3rd Down Def Rank", "Team", "Games", "Win-Loss","Opp 3rd Conversion", "Opp 3rd Attempt", "Opponent 3rd Percent"],
    "4th Down Conversion Pct": ["4th Down Rank", "Team", "Games", "Win-Loss","4th Attempts", "4th Conversions", "4th Percent"],
    "4th Down Conversion Pct Defense": ["4rd Down Def Rank", "Team", "Games", "Win-Loss","Opp 4th Conversion", "Opp 4th Attempt", "Opponent 4th Percent"],
}

JOIN_COLS = ["Team", "Games", "Win-Loss"]

def scrape_stat_category(stat_group):
    # needs to be local for multiprocessing
    driver = webdriver.Chrome('C:\\tools\\chromedriver\\chromedriver.exe')

    # Go to the Starting page
    driver.get(stats_url)
    time.sleep(2)

    sport_select = Select(driver.find_element(By.NAME, "sport"))
    sport_select.select_by_value("MFB")
    time.sleep(1)

    # TODO: Figure out how to select the year
    # year_select = Select(driver.find_element(By.NAME, "acadyr"))
    # year_select.select_by_value("2022-23")

    div_select = Select(driver.find_element(By.NAME, "u_div"))
    div_select.select_by_value("11.0")
    time.sleep(1)

    # Find the team tab
    team_tab = driver.find_element(By.ID, "stat_type_T_N")
    team_tab.click()
    time.sleep(2)

    print(f"Scraping {stat_group}...")
    stat = driver.find_element(By.ID, "Stats")
    stat.click()

    # Select the stat group
    stat.send_keys(stat_group)
    stat.send_keys(Keys.RETURN)
    time.sleep(1.5)

    # Now we can see the full table, just need to see all 150 rows
    len = driver.find_element(By.NAME, "rankings_table_length")
    len.click()
    len.send_keys(Keys.DOWN)
    len.send_keys(Keys.RETURN)
    time.sleep(1.5)

    # Now we can rip the entire table (there's 2, we just want the latter)
    dfs = pd.read_html(driver.page_source)[1]

    # Rename the columns
    dfs.columns = STAT_GROUPS[stat_group]

    # Write to CSV
    dfs.to_csv(f"scraping/{stat_group}.csv", index=False)

# for stat_group in STAT_GROUPS:
#     scrape_stat_category(stat_group)

# Once we are done scraping we can merge all the csvs into one
dfs = []
for stat_group in STAT_GROUPS:
    df = pd.read_csv(f"scraping/{stat_group}.csv")
    dfs.append(df)

# Merge all the dataframes
df = dfs[0]
for i in range(1, len(dfs)):
    df = df.merge(dfs[i], on=JOIN_COLS)

print(df)
df.to_csv("data/cfb22.csv", index=False)
print("Done scraping!")