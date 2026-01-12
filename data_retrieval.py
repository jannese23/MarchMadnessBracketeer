import csv
from datetime import date, timedelta
import http.client
import json
import time

def make_school_key():
    data = get_data_json("/schools-index")
    with open("school_key.csv", "w", newline="") as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(["slug", "name", "long"])
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
            if not (slug == "" and name == "" and long == ""):
                csv_writer.writerow([
                    slug,
                    name,
                    long
                ])

def append_list_as_row(list_of_elem):
    with open("games.csv", "a", newline="") as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(list_of_elem)

def append_sd_to_csv(year, month, day):
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
            append_list_as_row([
                gameID,
                gameURL,
                awayTeam,
                awayScore,
                awayRank,
                homeTeam,
                homeScore,
                homeRank
            ])


def get_schedule_day(year, month, day):
    path = f"/scoreboard/basketball-men/d1/{year:04d}/{month:02d}/{day:02d}/all-conf"
    return get_data_json(path)

def get_game_scores(gameID_Url):
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
    d = start_date
    while d <= end_date:
        yield d
        d += timedelta(days=1)


def fetch_games_in_date_range():
    print("Enter start date (YYYY-MM-DD): ")
    start_input = input()
    print("Enter end date (YYYY-MM-DD): ")
    end_input = input()

    start_date = date.fromisoformat(start_input)
    end_date = date.fromisoformat(end_input)

    for d in date_generator(start_date, end_date):
        append_sd_to_csv(d.year, d.month, d.day)



def get_data_json(path):
    raw_data = get_data_text(path)
    text = raw_data.decode('utf-8')
    return json.loads(text)

def get_data_text(path):
    conn = http.client.HTTPSConnection("ncaa-api.henrygd.me")
    try:
        raw_data = call_api(conn, path)
    finally:
        conn.close()
    return raw_data
    
def call_api(conn, path, verbose=False, pause=0.25):
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
    #make_school_key()
    #print(get_data_json("/game/6291328/team-stats"))
    fetch_games_in_date_range()