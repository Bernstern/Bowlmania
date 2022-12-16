library(tidyverse)
library(RSelenium)
library(readxl)
library(rvest)
library(XML)

conn <- rsDriver(browser = "chrome",
    port = 4445L,
    )

conn$client$getStatus()

chooseStat <- c("Total Offense", 
  "Total Defense", 
  "3rd Down Conversion Pct", 
  "3rd Down Conversion Pct Defense", 
  "4th Down Conversion Pct", 
  "4th Down Conversion Pct Defense",
  "Fewest Penalty Yards Per Game",
  "First Down Defense",
  "First Down Offense",
  "Kickoff Return Defense",
  "Kickoff Return",
  "Passing Offense",
  "Passing Yards Allowed",
  "Punt Return Defense",
  "Punt Return",
  "Red Zone Defense",
  "Red Zone Offense",
  "Rushing Defense",
  "Rushing Offense",
  "Scoring Defense",
  "Scoring Offense",
  "Sacks Allowed",
  "Team Tackles for Loss",
  "Time of Possession",
  "Turnover Margin"
  )

year <- c("2022-23")

for (j in 1:10) {
  
  for (i in 1:25) {
    
    conn$client$navigate("https://stats.ncaa.org/")
    
    Sys.sleep(2)
    
    sportInput <- conn$client$findElement(using = "css", "[name = 'sport_code_select_chosen']")
    sportInput$clickElement()
    sportInput$sendKeysToElement(list("football", key = "enter"))
    
    Sys.sleep(3)
    
    yearInput <- conn$client$findElement(using = "css", "[name = 'acadyr']")
    yearInput$clickElement()
    yearInput$sendKeysToElement(list(year[j], key = "enter"))
    
    Sys.sleep(3)
    
    divInput <- conn$client$findElement(using = "css", "[name = 'u_div']")
    divInput$clickElement()
    divInput$sendKeysToElement(list("FBS", key = "enter"))
    
    Sys.sleep(3)
    
    selectTeam <- conn$client$findElement(using = "css", "[id = 'stat_type_T_N']")
    selectTeam$clickElement()
    
    Sys.sleep(3)
    
    statInput <- conn$client$findElement(using = "css",
                                         "[id = 'Stats']")
    statInput$clickElement()
    statInput$sendKeysToElement(list(chooseStat[i], key = "enter"))
    
    Sys.sleep(5)
    
    lenInput <- conn$client$findElement(using = "css selector",
                                    "[name='rankings_table_length']")
    
    lenInput$clickElement()
    lenInput$sendKeysToElement(list(key = "down_arrow"))
    lenInput$sendKeysToElement(list(key = "enter"))
    
    Sys.sleep(4)
    
    tbl <- conn$client$getPageSource()[[1]] %>% 
      readHTMLTable()
    
    stat_tbl <- tbl$rankings_table
    
    assign(str_replace_all(chooseStat[i], " ", "_"), stat_tbl)
  }
  
  colnames(Total_Offense) <- c("Off Rank", "Team", "Games", "Win-Loss", "Off Plays", "Off Yards", "Off Yards/Play", "Off TDs", "Off Yards per Game")
  colnames(Total_Defense) <- c("Def Rank", "Team", "Games", "Win-Loss", "Def Plays", "Yards Allowed", "Yards/Play Allowed", "Off TDs Allowed", "Total TDs Allowed", "Yards Per Game Allowed" )
  colnames(Turnover_Margin) <- c("Turnover Rank", "Team", "Games", "Win-Loss", "Fumbles Recovered", "Opponents Intercepted", "Turnovers Gain", "Fumbles Lost", "Interceptions Thrown", "Turnovers Lost", "Turnover Margin", "Avg Turnover Margin per Game")
  colnames(Time_of_Possession) <- c("Time of Possession Rank", "Team", "Games", "Win-Loss", "Time of Possession", "Average Time of Possession per Game")
  colnames(Team_Tackles_for_Loss) <- c("Tackle for Loss Rank", "Team", "Games", "Win-Loss", "Solo Tackle For Loss", "Assist Tackle For Loss", "Tackle for Loss Yards", "Total Tackle For Loss", "Tackle For Loss Per Game")
  colnames(Sacks_Allowed) <- c("Sack Rank", "Team", "Games", "Win-Loss",  "Sacks", "Sack Yards", "Average Sacks per Game" )
  colnames(Scoring_Offense) <- c("Scoring Off Rank", "Team", "Games",    "Win-Loss", "Touchdowns", "PAT", "2 Point Conversions", "Defensive Points", "Feild Goals", "Safety", "Total Points", "Points Per Game" )
  colnames(Scoring_Defense) <- c("Scoring Def Rank", "Team", "Games",   "Win-Loss", "Touchdowns Allowed", "Opponent Extra Points",  "2 Point Conversions Allowed", "Opp Deflected Extra Points", "Opp Feild Goals Made", "Opp Safety", "Points Allowed", "Avg Points per Game Allowed" )
  colnames(Rushing_Offense) <- c("Rushing Off Rank", "Team", "Games", "Win-Loss", "Rush Attempts", "Rush Yds", "Yards/Rush", "Rushing TD",  "Rushing Yards per Game"  )
  colnames(Rushing_Defense) <- c("Rushing Def Rank", "Team", "Games", "Win-Loss", "Opp Rush Attempts", "Opp Rush Yards Alloweed", "Yds/Rush Allowed",     "Opp Rush Touchdowns Allowed", "Rush Yards Per Game Allowed")
  colnames(Red_Zone_Offense) <- c("Redzone Off Rank", "Team",  "Games"   ,"Win-Loss", "Redzone Attempts","Redzone Rush TD", "Redzone Pass TD", "Redzone Field Goals Made", "Redzone Scores", "Redzone Points")
  colnames(Red_Zone_Defense) <- c("Redzone Def Rank", "Team", "Games", "Win-Loss", "Opp Redzone Attempts", "Opp Redzone Rush TD Allowed",
  "Opp Redzone Pass Touchdowns Allowed", "Opp Redzone Field Goals Made", "Opp Redzone Scores", "Redzone Points Allowed")
  colnames(Punt_Return) <- c("Punt Return Rank", "Team", "Games", "Win-Loss", "Punt Returns", "Net Punt Return Yards", "Punt Return Touchdowns", "Avg Yards Per Punt Return" )
  colnames(Punt_Return_Defense) <- c("Punt Return Def Rank", "Team", "Games",  "Win-Loss", "Opp Punt Returns", "Opp Net Punt Return Yards",
   "Opp Punt Return Touchdowns Allowed", "Avg Yards Allowed per Punt Return")
  colnames(Passing_Offense) <- c("Passing Off Rank", "Team", "Games", "Win-Loss", "Pass Attempts", "Pass Completions", "Interceptions Thrown",  "Pass Yards", "Pass Yards/Attempt",  "Yards/Completion", "Pass Touchdowns", "Pass Yards Per Game")
  colnames(Passing_Yards_Allowed) <- c("Pass Def Rank", "Team", "Games",  "Win-Loss", "Opp Completions Allowed", "Opp Pass Attempts", "Opp Pass Yds Allowed", "Opp Pass TDs Allowed", "Yards/Attempt Allowed", "Yards/Completion Allowed", "Pass Yards Per Game Allowed")
  colnames(Kickoff_Return) <- c("Kickoff Return Rank", "Team", "Games", "Win-Loss","Kickoffs Returned", "Kickoff Return Yards", "Kickoff Return Touchdowns", "Avg Yard per Kickoff Return" )
  colnames(Kickoff_Return_Defense) <- c("Kickoff Return Def Rank", "Team", "Games", "Win-Loss", "Opp Kickoff Returns","Kickoff Touchbacks", "Opponent Kickoff Return Yards", "Opp Kickoff Return Touchdowns Allowed", "Avg Yards per Kickoff Return Allowed")
  colnames(First_Down_Offense) <- c("First Down Rank", "Team", "Games","Win-Loss", "First Down Runs", "First Down Passes", "First Down Penalties", "First Downs" )
  colnames(First_Down_Defense) <- c("First Down Def Rank", "Team", "Games","Win-Loss", "Opp First Down Runs", "Opp First Down Passes", "Opp First Down Penalties", "Opp First Downs" )
  colnames(Fewest_Penalty_Yards_Per_Game) <- c("Penalty Rank", "Team", "Games", "Win-Loss", "Penalties", "Penalty Yards", "Penalty Yards Per Game")
  colnames(`3rd_Down_Conversion_Pct`) <- c("3rd Down Rank", "Team", "Games", "Win-Loss","3rd Attempts", "3rd Conversions", "3rd Percent")
  colnames(`3rd_Down_Conversion_Pct_Defense`) <- c("3rd Down Def Rank", "Team", "Games", "Win-Loss","Opp 3rd Conversion", "Opp 3rd Attempt", "Opponent 3rd Percent")
  colnames(`4th_Down_Conversion_Pct`) <- c("4th Down Rank", "Team", "Games", "Win-Loss","4th Attempts", "4th Conversions", "4th Percent")
  colnames(`4th_Down_Conversion_Pct_Defense`) <- c("4rd Down Def Rank", "Team", "Games", "Win-Loss","Opp 4th Conversion", "Opp 4th Attempt", "Opponent 4th Percent")
  
  
  cfb <- merge(Total_Offense, Total_Defense, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, First_Down_Offense, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, First_Down_Defense, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, `4th_Down_Conversion_Pct`, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, `4th_Down_Conversion_Pct_Defense`, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Kickoff_Return, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Kickoff_Return_Defense, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Passing_Offense, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Passing_Yards_Allowed, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Fewest_Penalty_Yards_Per_Game, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Punt_Return, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Punt_Return_Defense, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Red_Zone_Offense, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Red_Zone_Defense, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Rushing_Offense, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Rushing_Defense, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Sacks_Allowed, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Scoring_Defense, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Scoring_Offense, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Team_Tackles_for_Loss, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, `3rd_Down_Conversion_Pct`, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, `3rd_Down_Conversion_Pct_Defense`, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Time_of_Possession, by=c("Team", "Games", "Win-Loss"))
  cfb <- merge(cfb, Turnover_Margin, by=c("Team", "Games", "Win-Loss"))
  
  
  rm(First_Down_Offense, First_Down_Defense, `4th_Down_Conversion_Pct`, 
     `4th_Down_Conversion_Pct_Defense`, Total_Defense, Total_Offense, Kickoff_Return, 
     Kickoff_Return_Defense, Passing_Offense, Passing_Yards_Allowed, Fewest_Penalty_Yards_Per_Game, 
     Punt_Return, Punt_Return_Defense, Red_Zone_Defense, Red_Zone_Offense, Rushing_Defense, Rushing_Offense,
     Sacks_Allowed, Scoring_Defense, Scoring_Offense, Team_Tackles_for_Loss, `3rd_Down_Conversion_Pct`,
     `3rd_Down_Conversion_Pct_Defense`, Time_of_Possession, Turnover_Margin)
  
  
  assign(paste0("cfb", year[j]), cfb)
}