from datetime import date, timedelta
import http.client
import json
import keyboard
import sqlite3
import time
import api
import query

last_call_ts = 0
ADDRESS = "ncaa-api.henrygd.me"

# =======================
# * Database Population *
# =======================   FIX DATABASE ENTRY TO INPUT SEASON AS WELL

def populate_sql_games_in_date_range(database, start, end, manual=False, verbose=False):
    """
    Populate the games table in the database for a specified date range.
    
    :param database: Path to the SQLite database file.
    """
    if manual:
        print("Enter start date (YYYY-MM-DD): ")
        start_input = input()
        print("Enter end date (YYYY-MM-DD): ")
        end_input = input()

        start_date = date.fromisoformat(start_input)
        end_date = date.fromisoformat(end_input)
    else:
        start_date = start
        end_date = end

    db_conn = sqlite3.connect(database)
    db_cursor = db_conn.cursor()
    http_conn = http.client.HTTPSConnection(ADDRESS)

    db_cursor.execute('''CREATE TABLE IF NOT EXISTS games
                 (game_id INTEGER PRIMARY KEY, game_id_url TEXT, home_team_id TEXT, 
                  away_team_id INTEGER, home_score INTEGER, away_score INTEGER, 
                  conference_game INTEGER, game_date TEXT, season_year INTEGER)''')
    print("Retrieving all schedules")
    
    syear = end_date.year
    
    last_date = None
    for current_date in date_generator(start_date, end_date):
        print(f"Retrieved {current_date}", end="\r")
        try: 
            query.create_schedule_day_execution(current_date, syear, last_call_ts, db_cursor, http_conn)
        except Exception as e:
            print(f"\nError processing date {current_date}: {e}, last successful date: {last_date}. Aborting further processing.")
            http_conn.close()
            db_conn.commit()
            db_conn.close()
            return
        
        last_date = current_date
    try:
        db_conn.commit()
    except Exception as e:
        print(f"Error during final commit: {e}")
    
    http_conn.close()
    db_conn.close()

def populate_sql_boxscores(database, start, end):
    """
    Populate the boxscores table in the database. 
    The rate is ~70 game boxscores per minute

    :param database: Path to the SQLite database file.
    """
    db_conn = sqlite3.connect(database)
    db_cursor = db_conn.cursor()
    http_conn = http.client.HTTPSConnection(ADDRESS)

    db_cursor.execute('''CREATE TABLE IF NOT EXISTS game_boxscores
                         (game_id INTEGER, home_team_stats TEXT,
                          away_team_stats TEXT)''')
    
    db_conn.commit()
    
    game_id_urls = query.get_all_game_urls_query(database, start, end)

    game_count = len(game_id_urls)
    game_index = 1

    for game_id_url in game_id_urls:
        try:
            query.create_boxscore_execution(game_id_url, last_call_ts, db_cursor, http_conn)
            print(f"({game_index}/{game_count}) Game boxscores retrieved.    ", end="\r")
            if game_index % 100 == 0:
                try:
                    db_conn.commit()
                except Exception as e:
                    print(f"Error during intermediate commit: {e}")

        except Exception as e:
            print(f"Error processing boxscore for {game_id_url}: {e}. Continuing to next.")
        # KeyboardInterrupt handling can be added here if desired
        if keyboard.is_pressed('q'):
            print("Keyboard interrupt detected. Stopping boxscore population.")
            break
        game_index += 1
    
    try:
        db_conn.commit()
    except Exception as e:
        print(f"Error during final commit: {e}")
    http_conn.close()
    db_conn.close()

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
    data = api.get_data_json(f"{gameID_Url}/team-stats")
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

def get_season_range(year, last_call_ts=0):
    """
    Gets the date range of a NCAA season prior to a March Madness tournament

    :param year: Year of March Madness tournament
    :returns tuple:
    """
    
    http_conn = http.client.HTTPSConnection(ADDRESS)

    tempDate = date(year-1, 11, 3)
    args = {'date': tempDate}
    scheduleDay, last_call_ts = api.get_specified_data('schedule', args, last_call_ts, http_conn)
    if scheduleDay:
        scheduleLen = len(scheduleDay['games'])
    else:
        scheduleLen = 0

    while scheduleLen == 0:
        tempDate += timedelta(days=1)
        args['date'] = tempDate
        scheduleDay, last_call_ts = api.get_specified_data('schedule', args, last_call_ts, http_conn)
        if scheduleDay:
            scheduleLen = len(scheduleDay['games'])
        else:
            scheduleLen = 0

    checkDate = tempDate + timedelta(days=-1)
    args['date'] = checkDate
    scheduleDay, last_call_ts = api.get_specified_data('schedule', args, last_call_ts, http_conn)
    if scheduleDay:
        scheduleLen = len(scheduleDay['games'])
    else:
        scheduleLen = 0

    while scheduleLen != 0:
        tempDate = checkDate
        checkDate += timedelta(days=-1)
        args['date'] = checkDate
        scheduleDay, last_call_ts = api.get_specified_data('schedule', args, last_call_ts, http_conn)
        if scheduleDay:
            scheduleLen = len(scheduleDay['games'])
        else:
            scheduleLen = 0
    
    start = tempDate
    print(f"Start date: {start}")

    tempDate = date(year, 3, 1)
    
    args['date'] = tempDate
    scheduleDay, last_call_ts = api.get_specified_data('schedule', args, last_call_ts, http_conn)
    if scheduleDay and len(scheduleDay['games']):
        bracketRound = check_bracket_round(scheduleDay['games'])
    else:
        bracketRound = ''

    while bracketRound == '':
        tempDate += timedelta(days=1)
        args['date'] = tempDate
        scheduleDay, last_call_ts = api.get_specified_data('schedule', args, last_call_ts, http_conn)
        if scheduleDay and len(scheduleDay['games']):
            bracketRound = check_bracket_round(scheduleDay['games'])   
        else:
            bracketRound = ''
    
    http_conn.close()
    end = tempDate
    print(f"End Date: {end}")
    return start, end

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

def one_year_retrieval_workflow(year, manual=False):
    """
    Generate data in SQLite db on local computer for one CBB season.
    
    :param year: Year of tournament
    """
    if manual:
        year = int(input("Enter Year (YYYY): "))
    print(f"Retrieving games prior to {year} March Madness Tournament")
    start, end = get_season_range(year)

    populate_sql_games_in_date_range("data/games.db", start, end)
    populate_sql_boxscores("data/games.db", start, end)
    print("Finished retrieving")

if __name__ == "__main__":
    one_year_retrieval_workflow(0, manual=True)
    
    