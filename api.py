import json
import http.client

ADDRESS = "ncaa-api.henrygd.me"

def get_specified_data(type, args, http_conn=None):

    match type:
        case "schedule":
            year = args['date'].year
            month = args['date'].year
            day = args['date'].year
            path = f"/scoreboard/basketball-men/d1/{year:04d}/{month:02d}/{day:02d}/all-conf"
        case "boxscore":
            game_id_url = args['game_id_url']
            path = f"{game_id_url}/boxscore"

    return get_data_json(path, http_conn)

def get_data_json(path, http_conn=None):
    """
    Gets JSON data from the API.
    
    :param path: API endpoint path.
    :return: Parsed JSON data.
    """
    if http_conn is None:
        conn = http.client.HTTPSConnection(ADDRESS)
    else: 
        conn = http_conn

    try:
        raw_data = call_api(conn, path)
    finally:
        conn.close()

    text = raw_data.decode('utf-8')
    return json.loads(text)

def call_api(conn, path, verbose=False):
    """
    Calls the API and retrieves raw data.
    
    :param conn: HTTP connection object.
    :param path: API endpoint path.
    :param verbose: Boolean flag for debugging output.
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

    return raw_data

