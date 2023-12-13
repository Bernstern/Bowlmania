# Bowlmania - BernGPT

This is project I've done for the past few years to predict the outcomes of the NCAA bowl games. This year we heavily leveraged Hex and a very helpful python package `cfbd` to analyze the data and aggregate game data respectively.

# Contributors

I would like to aknowledge two of my friends who helped me with this project.

- [ezipe](https://github.com/ezipe)
- [RyanD893](https://github.com/RyanD893)

# Process

The whole process anchors on getting the last 10 years of CFB games and those teams stats for that year, then training a model on that data and using that model to pick the winner of future games, in this case the bowl games.

## Data Collection

### Team Performance

To get team performance data I wrote a scraper using `pandas` and `selenium` to scrape the NCAA website for the last 10 years of team performance data.

### Game Data

To get game data I used the `cfbd` python package to get the last 10 years of game data. This was a lot easier than scraping the NCAA website. Huge shoutout to the creator of that package.

### Pre-Processing

The hardest part of pre-processing was getting normalization on team names to work, many teams have a shorthand or abbreviation that is used in the game data but not in the performance data. I ended up making some facilities in Hex to make this process easier but it was still very manual

> Note that some games in the last 10 years are excluded because the performance data is not available for those teams. This is a small number of games and should not affect the model too much. Mostly D2 and D3 teams.

## Training

For training I made some tools in Hex to visualize model performance and confidence, and then pretty much tried a variety of pipelines and models until I found one that worked well.

## Ranking

Part of using `sklearn` is that it has a built in `predict_proba` function that returns the probability of each class. I used this to rank the teams in each bowl game based on how confident my model was in each prediction.

# Shortcomings

- My model was either very confident or very unconfident in its predictions. Meaning that it was either very sure a team would win or very sure a team would lose. This is a problem because it is very hard to rank teams when there is a large gap between the most confident and least confident prediction. I am not sure how to best remedy this other than getting more performance data to be able to train on more years of bowl games.
- I was interested in also making a general game predictor given how a team has performed the last 4 years (assuming some of those playesrs would still be on the team/skill carryover) but this proved beyond the scope of the project.

# Results

I should probably have a confussion matrix here but I was too tired to make one. Check out this bar graph.

## Testing Confidence

This image shows the confidence curves of all the models I evaluated :

![Confidence Curves]("resources/relative_confidence.png")

## Predictions

The bolded team is my predicted winner along with how my model ranked that pick.

|     | Team A             | Team B              | Projected Winner   | Ranked Confidence | Confidence % |
| --: | :----------------- | :------------------ | :----------------- | ----------------: | -----------: |
|   0 | ga southern        | ohio                | ohio               |                 9 |     0.591825 |
|   1 | howard             | florida am          | florida am         |                30 |     0.794975 |
|   2 | jacksonville state | louisiana           | jacksonville state |                36 |     0.875496 |
|   3 | miami oh           | app state           | miami oh           |                38 |     0.891484 |
|   4 | new mexico         | fresno state        | fresno state       |                35 |     0.868388 |
|   5 | ucla               | boise state         | ucla               |                15 |     0.653845 |
|   6 | california         | texas tech          | texas tech         |                 8 |      0.59097 |
|   7 | western ky         | old dominion        | western ky         |                24 |     0.719515 |
|   8 | utsa               | marshall            | utsa               |                37 |     0.883676 |
|   9 | south fla          | syracuse            | south fla          |                16 |      0.65527 |
|  10 | georgia tech       | ucf                 | georgia tech       |                13 |     0.641005 |
|  11 | arkansas state     | niu                 | arkansas state     |                26 |     0.762537 |
|  12 | troy               | duke                | troy               |                40 |      0.93696 |
|  13 | georgia state      | utah state          | georgia state      |                23 |     0.708443 |
|  14 | james madison      | air force           | james madison      |                33 |     0.823555 |
|  15 | south alabama      | eastern mich        | south alabama      |                31 |     0.808177 |
|  16 | utah               | northwestern        | utah               |                25 |     0.724196 |
|  17 | coastal carolina   | san jose state      | coastal carolina   |                22 |     0.701098 |
|  18 | bowling green      | minnesota           | bowling green      |                18 |     0.662641 |
|  19 | texas state        | rice                | texas state        |                14 |     0.648838 |
|  20 | kansas             | unlv                | kansas             |                 1 |     0.504707 |
|  21 | virginia tech      | tulane              | tulane             |                39 |     0.893582 |
|  22 | north carolina     | west virginia       | north carolina     |                28 |     0.777974 |
|  23 | louisville         | southern california | louisville         |                41 |     0.942676 |
|  24 | texas am           | oklahoma state      | texas am           |                 7 |     0.559571 |
|  25 | smu                | boston college      | smu                |                42 |     0.961554 |
|  26 | rutgers            | miami fl            | miami fl           |                 3 |      0.53502 |
|  27 | nc state           | kansas state        | nc state           |                34 |     0.830115 |
|  28 | arizona            | oklahoma            | arizona            |                10 |     0.604964 |
|  29 | clemson            | kentucky            | clemson            |                27 |      0.77038 |
|  30 | oregon state       | notre dame          | notre dame         |                 2 |     0.507549 |
|  31 | memphis            | iowa state          | memphis            |                32 |     0.822096 |
|  32 | missouri           | ohio state          | missouri           |                 6 |      0.55559 |
|  33 | ole miss           | penn state          | ole miss           |                21 |     0.696878 |
|  34 | auburn             | maryland            | maryland           |                 4 |     0.537704 |
|  35 | georgia            | florida state       | georgia            |                 5 |       0.5452 |
|  36 | toledo             | wyoming             | toledo             |                29 |     0.785772 |
|  37 | wisconsin          | lsu                 | lsu                |                20 |      0.69092 |
|  38 | iowa               | tennessee           | iowa               |                17 |     0.655844 |
|  39 | liberty            | oregon              | liberty            |                19 |     0.664697 |
|  40 | alabama            | michigan            | alabama            |                12 |      0.61886 |
|  41 | texas              | washington          | texas              |                11 |     0.611484 |
