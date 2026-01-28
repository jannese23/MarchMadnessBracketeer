from datetime import date, timedelta
import http.client
import json
import keyboard
import sqlite3
import time

# ======================
# * API Data Retrieval *
# ======================

def get_data_json(path):
    """
    Gets JSON data from the API.
    
    :param path: API endpoint path.
    :return: Parsed JSON data.
    """
    raw_data = get_data_text(path)
    text = raw_data.decode('utf-8')
    return json.loads(text)

def get_data_text(path):
    """
    Gets raw data from the API.
    
    :param path: Description
    :return: Raw data as bytes.
    """
    conn = http.client.HTTPSConnection("ncaa-api.henrygd.me")
    try:
        raw_data = call_api(conn, path)
    finally:
        conn.close()
    return raw_data
    
def call_api(conn, path, verbose=False, pause=0.25):
    """
    Calls the API and retrieves raw data.
    
    :param conn: HTTP connection object.
    :param path: API endpoint path.
    :param verbose: Boolean flag for debugging output.
    :param pause: Pause duration in seconds between calls. (default 0.25s because of 4 calls/sec rate limit)
    :return: Raw data as bytes.
    """
    conn.request("GET", path)
    response = conn.getresponse()
    raw_data = response.read()

    if(response.status != 200):
        preview = raw_data[:100].decode('utf-8', errors="replace")
        raise Exception(f"API request failed: {response.status} {response.reason}. Body preview: {preview}")
    
    if verbose:
        print("Raw data retrieved:")
        print("Bytes received:", len(raw_data))
    
    time.sleep(pause)
    return raw_data

def get_schedule_day(year, month, day):
    path = f"/scoreboard/basketball-men/d1/{year:04d}/{month:02d}/{day:02d}/all-conf"
    try:
        get_data_json(path)
    except:
        return 0
    return get_data_json(path)

def get_game_boxscore(gameID_Url):
    """
    Get the boxscore data for a specific game.
    
    :param gameID_Url: Game URL.
    :return: Boxscore JSON data.
    """
    return get_data_json(f"{gameID_Url}/boxscore")

# =======================
# * Database Population *
# =======================   FIX DATABASE ENTRY TO INPUT SEASON AS WELL

def make_school_key():
    """
    Make a school key database from the /schools-index endpoint.
    """
    data = get_data_json("/schools-index")
    conn = sqlite3.connect('school_key.db')

    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS school_key
                    (slug TEXT PRIMARY KEY, name TEXT, longname TEXT)''')
    
    for school in data:
        try:
            slug = school['slug']
        except KeyError:
            slug = ""
        try:
            name = school['name']
        except KeyError:
            name = ""
        try:
            long = school['long']
        except KeyError:
            long = ""

        c.execute('''INSERT OR IGNORE INTO school_key (slug, name, longname)
                VALUES (?, ?, ?)''', (slug, name, long))
    
    conn.commit()
    conn.close()

def populate_sql_games_in_date_range(database, start, end, verbose=False):
    """
    Populate the games table in the database for a specified date range.
    
    :param database: Path to the SQLite database file.
    """
    if verbose:
        print("Enter start date (YYYY-MM-DD): ")
        start_input = input()
        print("Enter end date (YYYY-MM-DD): ")
        end_input = input()

        start_date = date.fromisoformat(start_input)
        end_date = date.fromisoformat(end_input)
    else:
        start_input = start
        end_input = end

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS games
                 (gameID TEXT PRIMARY KEY, gameURL TEXT, awayTeam TEXT, awayScore INTEGER
                    , awayRank INTEGER, homeTeam TEXT, homeScore INTEGER, homeRank INTEGER, game_date DATE)''')

    last_date = None
    for current_date in date_generator(start_date, end_date):
        try: 
            create_game_sql_execution(current_date.year, current_date.month, current_date.day, c)
        except Exception as e:
            print(f"Error processing date {current_date}: {e}, last successful date: {last_date}. Aborting further processing.")
            conn.commit()
            conn.close()
            break
        last_date = current_date
    try:
        conn.commit()
    except Exception as e:
        print(f"Error during final commit: {e}")
    conn.close()

def populate_sql_boxscores(database, start, end):
    """
    Populate the boxscores table in the database.

    :param database: Path to the SQLite database file.
    """
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS boxscores
                    (gameURL TEXT, playerId TEXT, playerTeamId INTEGER, isHome BOOLEAN, starter BOOLEAN,
                    minutesPlayed INTEGER, fieldGoalsMade INTEGER, fieldGoalsAttempted INTEGER, fieldGoalPercentage REAL,
                    threePointsMade INTEGER, threePointsAttempted INTEGER, threePointPercentage REAL,
                    freeThrowsMade INTEGER, freeThrowsAttempted INTEGER, freeThrowPercentage REAL,
                    offensiveRebounds INTEGER, totalRebounds INTEGER, assists INTEGER, turnovers INTEGER,
                    personalFouls INTEGER, steals INTEGER, blockedShots INTEGER, points INTEGER,
                    PRIMARY KEY (gameURL, playerId))''')
    gameURLs = get_all_gameUrls(database, start, end)

    for gameURL in gameURLs:
        try:
            create_boxscore_sql_execution(gameURL, c)
            print(f"Processed boxscore for {gameURL}")
        except Exception as e:
            print(f"Error processing boxscore for {gameURL}: {e}. Continuing to next.")
        # KeyboardInterrupt handling can be added here if desired
        if keyboard.is_pressed('q'):
            print("Keyboard interrupt detected. Stopping boxscore population.")
            break
    
    try:
        conn.commit()
    except Exception as e:
        print(f"Error during final commit: {e}")
    conn.close()

# =====================
# * Create executions *
# =====================

def create_game_sql_execution(year, month, day, cursor):
    """
    Creates SQL execution for games on a specific day.

    :param year: Year of the game.
    :param month: Month of the game.
    :param day: Day of the game.
    :param cursor: SQLite cursor object.
    """

    sd = get_schedule_day(year, month, day)
    game_date = date(year, month, day).isoformat()

    for game in sd["games"]:
        if game['game']['gameState'] == "final":
            gameID = game['game']['url'].split("/game/")[1]
            gameURL = game['game']['url']
            awayTeam = game['game']['away']['names']['seo'] # away team SEO name for consistency
            awayScore = game['game']['away']['score']
            awayRank = game['game']['away']['rank']
            homeTeam = game['game']['home']['names']['seo'] # home team SEO name for consistency
            homeScore = game['game']['home']['score']
            homeRank = game['game']['home']['rank']

            if awayScore == '' or homeScore == '':
                awayScore, homeScore = get_game_scores(gameURL)
                with open("faulty_scores.txt", "a") as f:
                    f.write(f"{gameID}: {awayTeam} {awayScore} - {homeTeam} {homeScore}\n")

            cursor.execute('''INSERT OR IGNORE INTO games (gameID, gameURL, awayTeam, awayScore, awayRank,
                        homeTeam, homeScore, homeRank, game_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (gameID, gameURL, awayTeam, awayScore, awayRank,
                        homeTeam, homeScore, homeRank, game_date))

def create_boxscore_sql_execution(gameURL, cursor):
    boxscore = get_game_boxscore(gameURL)

    if boxscore['teams'][0]['isHome']:
        homeTeamId, awayTeamId = int(boxscore['teams'][0]['teamId']), int(boxscore['teams'][1]['teamId'])
    else:
        homeTeamId, awayTeamId = int(boxscore['teams'][1]['teamId']), int(boxscore['teams'][0]['teamId'])

    boxscore_data = dict()
    boxscore_data[boxscore['teamBoxscore'][0]['teamId']] = boxscore['teamBoxscore'][0]
    boxscore_data[boxscore['teamBoxscore'][1]['teamId']] = boxscore['teamBoxscore'][1]

    homePlayerStats = boxscore_data[homeTeamId]['playerStats']
    awayPlayerStats = boxscore_data[awayTeamId]['playerStats']  

    for player in homePlayerStats:
        playerTeamId = homeTeamId
        isHome = True
        playerId = player['lastName'] + "_" + str(player['id'])
        starter = True if player['starter'] else False

        minutesPlayed = int(player['minutesPlayed']) if player['minutesPlayed'] != '' else 0

        fgMade = int(player['fieldGoalsMade']) if player['fieldGoalsMade'] != '' else 0
        fgAttempted = int(player['fieldGoalsAttempted']) if player['fieldGoalsAttempted'] != '' else 0
        if fgAttempted > 0:
            fgPercentage = float(fgMade) / fgAttempted
        else:
            fgPercentage = 0.0

        threePMade = int(player['threePointsMade']) if player['threePointsMade'] != '' else 0
        threePAttempted = int(player['threePointsAttempted']) if player['threePointsAttempted'] != '' else 0
        if threePAttempted > 0:
            threePPercentage = float(threePMade) / threePAttempted
        else:
            threePPercentage = 0.0

        ftMade = int(player['freeThrowsMade']) if player['freeThrowsMade'] != '' else 0
        ftAttempted = int(player['freeThrowsAttempted']) if player['freeThrowsAttempted'] != '' else 0
        if ftAttempted > 0:
            ftPercentage = float(ftMade) / ftAttempted
        else:
            ftPercentage = 0.0

        offReb = int(player['offensiveRebounds']) if player['offensiveRebounds'] != '' else 0
        totReb = int(player['totalRebounds']) if player['totalRebounds'] != '' else 0
        assists = int(player['assists']) if player['assists'] != '' else 0
        turnovers = int(player['turnovers']) if player['turnovers'] != '' else 0
        personalFouls = int(player['personalFouls']) if player['personalFouls'] != '' else 0
        steals = int(player['steals']) if player['steals'] != '' else 0
        blocks = int(player['blockedShots']) if player['blockedShots'] != '' else 0
        points = int(player['points']) if player['points'] != '' else 0
    
        cursor.execute('''INSERT OR IGNORE INTO boxscores (gameURL, playerId, playerTeamId, isHome, starter,
                    minutesPlayed, fieldGoalsMade, fieldGoalsAttempted, fieldGoalPercentage, threePointsMade, 
                    threePointsAttempted, threePointPercentage, freeThrowsMade, freeThrowsAttempted, 
                    freeThrowPercentage, offensiveRebounds, totalRebounds, assists, turnovers, personalFouls, 
                    steals, blockedShots, points)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (gameURL, playerId, playerTeamId, isHome, starter,
                    minutesPlayed, fgMade, fgAttempted, fgPercentage, threePMade,
                    threePAttempted, threePPercentage, ftMade, ftAttempted,
                    ftPercentage, offReb, totReb, assists, turnovers, personalFouls,
                    steals, blocks, points))

    for player in awayPlayerStats:
        playerTeamId = awayTeamId
        isHome = False
        playerId = player['lastName'] + "_" + str(player['id'])
        starter = True if player['starter'] else False

        minutesPlayed = int(player['minutesPlayed']) if player['minutesPlayed'] != '' else 0

        fgMade = int(player['fieldGoalsMade']) if player['fieldGoalsMade'] != '' else 0
        fgAttempted = int(player['fieldGoalsAttempted']) if player['fieldGoalsAttempted'] != '' else 0
        if fgAttempted > 0:
            fgPercentage = float(fgMade) / fgAttempted
        else:
            fgPercentage = 0.0

        threePMade = int(player['threePointsMade']) if player['threePointsMade'] != '' else 0
        threePAttempted = int(player['threePointsAttempted']) if player['threePointsAttempted'] != '' else 0
        if threePAttempted > 0:
            threePPercentage = float(threePMade) / threePAttempted
        else:
            threePPercentage = 0.0

        ftMade = int(player['freeThrowsMade']) if player['freeThrowsMade'] != '' else 0
        ftAttempted = int(player['freeThrowsAttempted']) if player['freeThrowsAttempted'] != '' else 0
        if ftAttempted > 0:
            ftPercentage = float(ftMade) / ftAttempted
        else:
            ftPercentage = 0.0

        offReb = int(player['offensiveRebounds']) if player['offensiveRebounds'] != '' else 0
        totReb = int(player['totalRebounds']) if player['totalRebounds'] != '' else 0
        assists = int(player['assists']) if player['assists'] != '' else 0
        turnovers = int(player['turnovers']) if player['turnovers'] != '' else 0
        personalFouls = int(player['personalFouls']) if player['personalFouls'] != '' else 0
        steals = int(player['steals']) if player['steals'] != '' else 0
        blocks = int(player['blockedShots']) if player['blockedShots'] != '' else 0
        points = int(player['points']) if player['points'] != '' else 0

        cursor.execute('''INSERT OR IGNORE INTO boxscores (gameURL, playerId, playerTeamId, isHome, starter,
                    minutesPlayed, fieldGoalsMade, fieldGoalsAttempted, fieldGoalPercentage, threePointsMade, 
                    threePointsAttempted, threePointPercentage, freeThrowsMade, freeThrowsAttempted, 
                    freeThrowPercentage, offensiveRebounds, totalRebounds, assists, turnovers, personalFouls, 
                    steals, blockedShots, points)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (gameURL, playerId, playerTeamId, isHome, starter,
                    minutesPlayed, fgMade, fgAttempted, fgPercentage, threePMade,
                    threePAttempted, threePPercentage, ftMade, ftAttempted,
                    ftPercentage, offReb, totReb, assists, turnovers, personalFouls,
                    steals, blocks, points))


# ===================
# * Query Functions *
# ===================

def get_all_gameUrls(database, start, end):
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

# ====================
# * Helper Functions *        
# ====================

def date_generator(start_date, end_date):
    """Generate dates from start_date to end_date inclusive."""
    d = start_date
    while d <= end_date:
        yield d
        d += timedelta(days=1)

def get_game_scores(gameID_Url):
    """
    Get specific game scores from the team-stats endpoint.
    
    :param gameID_Url: Game URL.
    :return: Tuple of (awayScore, homeScore).
    """
    data = get_data_json(f"{gameID_Url}/team-stats")
    if data['status'] != 'F':
        return 0, 0
    
    team1 = data['teams'][0]
    team2 = data['teams'][1]

    Id_HA = {int(team1['teamId']): bool(team1['isHome']), int(team2['teamId']): bool(team2['isHome'])}

    teamABoxscore = data['teamBoxscore'][0]
    teamBBoxscore = data['teamBoxscore'][1]

    teamAStats = teamABoxscore['teamStats']
    teamBStats = teamBBoxscore['teamStats']

    teamAScore = (int(teamAStats['fieldGoalsMade']) - int(teamAStats['threePointsMade'])) * 2 + int(teamAStats['threePointsMade']) * 3 + int(teamAStats['freeThrowsMade'])
    teamBScore = (int(teamBStats['fieldGoalsMade']) - int(teamBStats['threePointsMade'])) * 2 + int(teamBStats['threePointsMade']) * 3 + int(teamBStats['freeThrowsMade'])

    if Id_HA[int(teamABoxscore['teamId'])]:
        homeScore = teamAScore
        awayScore = teamBScore 
    else:
        homeScore = teamBScore
        awayScore = teamAScore

    return awayScore, homeScore

def get_season_range(year):
    """
    Gets the date range of a NCAA season prior to a March Madness tournament

    :param year: Year of March Madness tournament
    :returns tuple:
    """
    tempDate = date(year-1, 11, 3)
    scheduleDay = get_schedule_day(tempDate.year, tempDate.month, tempDate.day)
    if scheduleDay:
        scheduleLen = len(scheduleDay['games'])
    else:
        scheduleLen = 0

    while scheduleLen == 0:
        tempDate += timedelta(days=1)
        scheduleDay = get_schedule_day(tempDate.year, tempDate.month, tempDate.day)
        if scheduleDay:
            scheduleLen = len(scheduleDay['games'])
        else:
            scheduleLen = 0

    checkDate = tempDate + timedelta(days=-1)
    scheduleDay = get_schedule_day(checkDate.year, checkDate.month, checkDate.day)
    if scheduleDay:
        scheduleLen = len(scheduleDay['games'])
    else:
        scheduleLen = 0

    while scheduleLen != 0:
        tempDate = checkDate
        checkDate += timedelta(days=-1)
        scheduleDay = get_schedule_day(checkDate.year, checkDate.month, checkDate.day)
        if scheduleDay:
            scheduleLen = len(scheduleDay['games'])
        else:
            scheduleLen = 0
    
    start = tempDate
    print(f"Start date: {start}")

    tempDate = date(year, 3, 1)
    
    scheduleDay = get_schedule_day(tempDate.year, tempDate.month, tempDate.day)
    if scheduleDay and len(scheduleDay['games']):
        bracketRound = check_bracket_round(scheduleDay['games'])
    else:
        bracketRound = ''

    while bracketRound == '':
        tempDate += timedelta(days=1)
        scheduleDay = get_schedule_day(tempDate.year, tempDate.month, tempDate.day)
        if scheduleDay and len(scheduleDay['games']):
            bracketRound = check_bracket_round(scheduleDay['games'])   
        else:
            bracketRound = ''
        
    end = tempDate
    print(f"End Date: {end}")

def check_bracket_round(games):
    for game in games:
        if 'FIRST FOUR' in game['game']['bracketRound']:
            return 'FIRST FOUR'
        elif game['game']['bracketRound'] == '':
            return ''
    return ''

# ======================
# * Workflow Execution *
# ======================

def one_year_retrieval_workflow(year):

    # First get range
    start, end = get_season_range(year)

    # Populate data
    populate_sql_games_in_date_range("data/games.db", start, end)
    populate_sql_boxscores("data/games.db", start, end)

if __name__ == "__main__":
    year = input("Enter Year: ")
    print(f"Processing games prior to {year} March Madness Tournament")
    one_year_retrieval_workflow(year)