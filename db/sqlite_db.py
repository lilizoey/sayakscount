import sqlite3
import datetime
from db.db_helpers import counts_handler
DB_NAME = "sqlite.db"

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

def initialize_db():
    """Initialize the database assuming it's empty."""
    c.execute("""
    CREATE TABLE IF NOT EXISTS UserCounts (
        Count INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER NOT NULL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS ChannelCounts (
        ChannelID INTEGER NOT NULL,
        MessageCount INTEGER NOT NULL,
        TimeStamp REAL NOT NULL,
        PRIMARY KEY (ChannelID)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS UserMessageCounts (
        UserID INTEGER NOT NULL,
        ChannelID INTEGER NOT NULL,
        MessageCount INTEGER NOT NULL,
        TimeStamp REAL NOT NULL,
        PRIMARY KEY (UserID, ChannelID)
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
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("INSERT INTO UserCounts (UserID) VALUES (?);", (userid,))
    conn.commit()
    count = c.execute("SELECT last_insert_rowid();").fetchone()[0]

    return count

def give_count(userid, count):
    """Give the user the specified count."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("UPDATE OR IGNORE UserCounts SET UserID = ? WHERE Count = ?;", (userid, count))
    conn.commit()

def add_messages_channel(channelid, time, message_count):
    """"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO ChannelCounts (ChannelID, MessageCount, TimeStamp) VALUES (?,?,?);",
              (channelid, message_count, time.timestamp()))
    conn.commit()

def get_channel_counts(channelid):
    """"""
    res = c.execute("SELECT TimeStamp, MessageCount FROM ChannelCounts WHERE ChannelID = ?;", (channelid,)).fetchone()
    return counts_handler(res)

def add_messages_user(userid, channelid, time, message_count):
    """Add the amount of messages for a user in a channel."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("INSERT OR REPLACE INTO UserMessageCounts (UserID, ChannelID, MessageCount, TimeStamp) VALUES (?,?,?,?);",
              (userid, channelid, message_count, time.timestamp()))
    conn.commit()

def get_message_counts(userid, channelid):
    """Get the timestamp for the message count for user in channel."""
    res = c.execute("SELECT TimeStamp, MessageCount FROM UserMessageCounts WHERE UserID = ? AND ChannelID = ?;",
                      (userid, channelid)).fetchone()
    return counts_handler(res)

def get_top_counts():
    """Get the userids for the top counts and the number of counts they have."""
    return c.execute("""
    SELECT COUNT(Count), UserID, 1.0 * COUNT(Count) / (SELECT COUNT(*) FROM UserCounts) AS percentage 
    FROM UserCounts 
    GROUP BY UserID 
    ORDER BY COUNT(Count) DESC 
    LIMIT 10;""").fetchall()

def get_entries():
    """Get all entries in the database."""
    return c.execute("""
    SELECT SUM(count) FROM
    (SELECT COUNT(*) AS count FROM UserCounts
    UNION ALL
    SELECT COUNT(*) AS count FROM ChannelCounts
    UNION ALL
    SELECT COUNT(*) AS count FROM UserMessageCounts);
    """).fetchone()[0]