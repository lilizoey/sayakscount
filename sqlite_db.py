import sqlite3
conn = sqlite3.connect("sqlite.db")
c = conn.cursor()

def initialize_db():
    """Initialize the database assuming it's empty."""
    c.execute("""
    CREATE TABLE IF NOT EXISTS UserCounts (
        Count INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER NOT NULL
    )
    """)

    conn.commit()

def get_counts_for(userid):
    """Get all the counts for the user with userid."""
    return c.execute("SELECT Count FROM UserCounts WHERE UserID = ?;", (userid,))

def get_who_counted(count):
    """Gets the userid for the given count."""
    return c.execute("SELECT UserID FROM UserCounts WHERE Count = ?;", (count,)).fetchone()[0]

def do_count(userid):
    """Count once for user with userid."""
    c.execute("INSERT INTO UserCounts (UserID) VALUES (?);", (userid,))
    conn.commit()
    count = c.execute("SELECT last_insert_rowid();").fetchone()[0]

    return count

def give_count(userid, count):
    """Give the user the specified count."""
    c.execute("UPDATE OR IGNORE UserCounts SET UserID = ? WHERE Count = ?;", (userid, count))