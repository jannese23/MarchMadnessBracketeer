import json
import http.client
import time

ADDRESS = "ncaa-api.henrygd.me"

def get_specified_data(type, args, last_call_ts, http_conn=None):

    match type:
        case "schedule":
            date = args['date']
            year = date.year
            month = date.month
            day = date.day
            path = f"/scoreboard/basketball-men/d1/{year:04d}/{month:02d}/{day:02d}/all-conf"
            try:
                get_data_json(path, last_call_ts, http_conn)
            except:
                return 0, 0
        case "boxscore":
            game_id_url = args['game_id_url']
            path = f"{game_id_url}/boxscore"
            get_data_json(path, last_call_ts, http_conn)
    return get_data_json(path, last_call_ts, http_conn)

def get_data_json(path, last_call_ts, http_conn=None):
    """
    Gets JSON data from the API.
    
    :param path: API endpoint path.
    :return: Parsed JSON data.
    """
    if http_conn is None:
        conn = http.client.HTTPSConnection(ADDRESS)
    else: 
        conn = http_conn

    
    raw_data = call_api(conn, path, last_call_ts)
    text = raw_data.decode('utf-8')
    data = json.loads(text)

    new_ts = time.monotonic()

    return data, new_ts

def call_api(conn, path, last_call_ts, verbose=False):
    """
    Calls the API and retrieves raw data.
    
    :param conn: HTTP connection object.
    :param path: API endpoint path.
    :param verbose: Boolean flag for debugging output.
    :return: Raw data as bytes.
    """
    wait_time = 0.2 - (time.monotonic() - last_call_ts)
    if wait_time > 0:
        time.sleep(wait_time)

    conn.request("GET", path)
    response = conn.getresponse()
    raw_data = response.read()

    if(response.status != 200):
        preview = raw_data[:100].decode('utf-8', errors="replace")
        raise Exception(f"API request failed: {response.status} {response.reason}. Body preview: {preview}")
    
    if verbose:
        print("Raw data retrieved:")
        print("Bytes received:", len(raw_data))
    
    return raw_data


if __name__ == '__main__':
    print(get_data_json("/game/6501458", 0))
