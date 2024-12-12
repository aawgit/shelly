import sqlite3

# TODO: Implement the functions

def start_database():
    """Start and connect to SQLite database."""
    conn = sqlite3.connect('shelly.db')
    return conn

def initialize_database(conn):
    """Set up required tables."""
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS user_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT,
                result TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

def stop_database(conn):
    """Close the database connection."""
    conn.close()
