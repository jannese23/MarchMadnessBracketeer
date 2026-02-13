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