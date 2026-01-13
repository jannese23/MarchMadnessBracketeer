# NCAA Men's (and possibly Women's) Basketball March Madness Bracket Predicter

## Step 1. Data Retrieval

The first step in this process is to retrieve the data, which is done by using the https://ncaa-api.henrygd.me api. A period of time is chosen in YYYY-MM-DD to YYYY-MM-DD format where schedules from each day are pulled from the database. Each schedule contains each game from that day and for each game in the database, a subsequent boxscore is queried. 

## Step 2. Normalization

The second step is to normalize data for each team. Teams are given a baseline score for how good a team is at the start of March Madness. 