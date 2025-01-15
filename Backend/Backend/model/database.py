import sqlite3
import os

def get_db_connection(app):
    """Get a database connection."""
    db_path = app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app):
    """Initialize the database."""
    db_path = app.config['DATABASE']
    if not os.path.exists('instance'):
        os.makedirs('instance')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiment_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT NOT NULL,
            prediction TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
