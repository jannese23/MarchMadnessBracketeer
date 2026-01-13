import csv
from datetime import date, timedelta
import http.client
import json
import sqlite3
import time

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

def create_game_sql_execution(year, month, day, cursor):
    """
    Docstring for create_game_sql_execution

    :param year: Year of the game.
    :param month: Month of the game.
    :param day: Day of the game.
    :param cursor: SQLite cursor object.
    """
    sd = get_schedule_day(year, month, day)

    for game in sd["games"]:
        if game['game']['gameState'] == "final":
            gameID = game['game']['url'].split("/game/")[1]
            gameURL = game['game']['url']
            awayTeam = game['game']['away']['names']['short']
            awayScore = game['game']['away']['score']
            awayRank = game['game']['away']['rank']
            homeTeam = game['game']['home']['names']['short']
            homeScore = game['game']['home']['score']
            homeRank = game['game']['home']['rank']

            if awayScore == '' or homeScore == '':
                awayScore, homeScore = get_game_scores(gameURL)
                with open("faulty_scores.txt", "a") as f:
                    f.write(f"{gameID}: {awayTeam} {awayScore} - {homeTeam} {homeScore}\n")

            cursor.execute('''INSERT OR IGNORE INTO games (gameID, gameURL, awayTeam, awayScore, awayRank,
                        homeTeam, homeScore, homeRank)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                        (gameID, gameURL, awayTeam, awayScore, awayRank,
                        homeTeam, homeScore, homeRank))

def get_schedule_day(year, month, day):
    path = f"/scoreboard/basketball-men/d1/{year:04d}/{month:02d}/{day:02d}/all-conf"
    return get_data_json(path)

def get_game_scores(gameID_Url):
    """
    Docstring for get_game_scores
    
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

def date_generator(start_date, end_date):
    """Generate dates from start_date to end_date inclusive."""
    d = start_date
    while d <= end_date:
        yield d
        d += timedelta(days=1)


def populate_sql_games_in_date_range(database):
    """
    Docstring for populate_sql_games_in_date_range
    
    :param database: Path to the SQLite database file.
    """
    print("Enter start date (YYYY-MM-DD): ")
    start_input = input()
    print("Enter end date (YYYY-MM-DD): ")
    end_input = input()

    start_date = date.fromisoformat(start_input)
    end_date = date.fromisoformat(end_input)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS games
                 (gameID TEXT PRIMARY KEY, gameURL TEXT, awayTeam TEXT, awayScore INTEGER
                    , awayRank INTEGER, homeTeam TEXT, homeScore INTEGER, homeRank INTEGER)''')

    for d in date_generator(start_date, end_date):
        try: 
            create_game_sql_execution(d.year, d.month, d.day, c)
        except Exception as e:
            print(f"Error processing date {d}: {e}, last successful date: {last_date}. Aborting further processing.")
            conn.commit()
            conn.close()
        last_date = d
    
    conn.commit()
    conn.close()

def get_data_json(path):
    """
    Docstring for get_data_json
    
    :param path: API endpoint path.
    :return: Parsed JSON data.
    """
    raw_data = get_data_text(path)
    text = raw_data.decode('utf-8')
    return json.loads(text)

def get_data_text(path):
    """
    Docstring for get_data_text
    
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
    Docstring for call_api
    
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


if __name__ == "__main__":
    #append_sd_to_csv(2024, 3, 15)
    make_school_key()
    #print(get_data_json("/game/6291328/team-stats"))
    #fetch_games_in_date_range()