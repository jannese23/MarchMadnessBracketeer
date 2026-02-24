import sqlite3

# =============================================================================
# The structure of the SQLite database is as follows: 
# 
# games:
#     game_id = INTEGER
#     home_team_id = TEXT
#     away_team_id = TEXT
#     home_score = INTEGER
#     away_score = INTEGER
#     neutral_site = BOOLEAN
#     conference_game = BOOLEAN
#     game_date = TEXT
#     season_year = INTEGER -- This is the year of the March Madness Tournament
# 
# game_boxscores:
#     game_id = INTEGER
#     home_team_stats = TEXT -- This is the home team boxscore
#     away_team_stats = TEXT -- This is the away team boxscore
#     
# 
#     {home/away}_team_stats:
#         {player_stats: {
#             {player: {
#                 starter = BOOLEAN,
#                 minutesPlayed = REAL,
#                 fg_made = INTEGER,
#                 fg_attempted = INTEGER,
#                 threep_made = INTEGER,
#                 threep_attempted = INTEGER,
#                 ft_made = INTEGER,
#                 ft_attempted = INTEGER,
#                 points = INTEGER,
#                 o_rebounds = INTEGER,
#                 total_rebounds = INTEGER,
#                 assists = INTEGER,
#                 turnovers = INTEGER,
#                 pfouls = INTEGER,
#                 steals = INTEGER,
#                 blocks = INTEGER
#             },
#             player2:...}},
#         team_stats: {
#                 estimated_poss = REAL, -- ~ FGA - OREB + TO + (0.44 * FTA)
#                 off_eff = REAL -- PTS/POSS
#                 def_eff = REAL -- OPP_PTS/OPP_POSS
#                 fg_made = INTEGER,
#                 fg_attempted = INTEGER,
#                 threep_made = INTEGER,
#                 threep_attempted = INTEGER,
#                 ft_made = INTEGER,
#                 ft_attempted = INTEGER,
#                 efg = REAL, -- (FGM + 0.5 * 3PM)/FGA
#                 points = INTEGER
#                 o_rebounds = INTEGER,
#                 total_rebounds = INTEGER,
#                 oreb_rate = REAL, -- OREB/(OREB + OPP_DREB)
#                 assists = INTEGER,
#                 turnovers = INTEGER,
#                 to_rate = REAL, -- TO/POSS
#                 pfouls = INTEGER,
#                 steals = INTEGER,
#                 blocks = INTEGER,
#             }}
# 
# teams:
#     team_name_6char = TEXT,
#     season = INTEGER,
#     games = TEXT, -- All game_ids used to compute the stats
#     off_eff_stats = TEXT,
#     def_eff_stats = TEXT,
#     fg_stats = TEXT,
#     threep_stats = TEXT,
#     ft_stats = TEXT,
#     efg_stats = TEXT,
#     point_stats = TEXT,
#     oreb_stats = TEXT,
#     totalreb_stats = TEXT,
#     assist_stats = TEXT,
#     to_stats = TEXT,
#     pfoul_stats = TEXT,
#     steal_stats = TEXT,
#     block_stats = TEXT
# 
#     {type}_stats: 
#         {
#             n_games = INTEGER,
#             {type}_mean = REAL,
#             weighted_{type}_difference_mean = REAL, 
#             {type}_stdev = REAL,
#             opp_{type}_difference_mean = REAL, -- Change in value compared to 
#                                                   opponent means averaged
#             -- Every row will at least include these, among other stats
#         }



# =============
# * Insertion *
# =============
# games:
#     game_id = INTEGER
#     home_team_id = TEXT
#     away_team_id = TEXT
#     home_score = INTEGER
#     away_score = INTEGER
#     conference_game = BOOLEAN
#     game_date = TEXT
#     season_year = INTEGER -- This is the year of the March Madness Tournament

def create_schedule_day_execution(date, syear, cursor):
    schedule_day = get_schedule_day(date)
    if schedule_day:
        for game in schedule_day['games']:
            create_game_execution(date, syear, game, cursor)

def create_game_execution(date, syear, game_data, cursor):
    game = game_data['game']
    game_id = int(game['gameID'])
    home_team_id = game['home']['names']['6char']
    away_team_id = game['away']['names']['6char']
    home_score = game['home']['score']
    away_score = game['away']['score']

    home_confs = game['home']['conferences']
    away_confs = game['away']['conferences']
    cond1 = home_confs['conferenceName'] == away_confs['conferenceName']
    cond2 = home_confs['conferenceSeo'] == away_confs['conferenceSeo']
    if cond1 or cond2:
        conference_game = True
    else:
        conference_game = False

    game_date = date
    season_year = syear

    cursor.execute('''INSERT OR IGNORE INTO games (game_id, home_team_id, 
                   away_team_id, home_score, away_score, conference_game,
                   game_date, season_year) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (game_id, home_team_id, away_team_id, home_score, 
                    away_score, conference_game, game_date, season_year))



# ================
# * Query Helper *
# ================

def get_all_gameUrls_query(database, start, end):
    """
    Get all game URLs from the database.
    
    :param database: Path to the SQLite database file.
    :return: List of all game URLs.
    """

    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("""SELECT gameURL FROM games 
                 WHERE game_date BETWEEN ? AND ? 
                 order by game_date ASC""", (start, end))
    rows = c.fetchall()
    conn.close()

    return [row[0] for row in rows]